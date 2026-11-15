// SPDX-License-Identifier: BSD-3-Clause
// A socket-activated, one-request account provisioner. No desktop runs as root.
#include <array>
#include <cerrno>
#include <cstring>
#include <csignal>
#include <algorithm>
#include <fcntl.h>
#include <fstream>
#include <grp.h>
#include <pwd.h>
#include <regex>
#include <stdexcept>
#include <string>
#include <string_view>
#include <sys/file.h>
#include <sys/prctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
#include <vector>
#include <pwquality.h>

namespace {
constexpr const char *state = "/var/lib/uke-cutefish-firstboot";
void need(bool ok, const char *message) { if (!ok) throw std::runtime_error(message); }
void wipe(std::string &s) { if (!s.empty()) explicit_bzero(s.data(), s.size()); }
bool clean(const std::string &s, size_t maximum) {
    if (s.empty() || s.size() > maximum) return false;
    for (unsigned char c : s) if (c < 32 || c == 127) return false;
    return true;
}
bool username(const std::string &s) {
    return std::regex_match(s, std::regex("[a-z_][a-z0-9_-]{0,31}"));
}
bool validTimezone(const std::string &s) {
    return s == "UTC" || std::regex_match(s, std::regex("[A-Za-z_+-]+(/[A-Za-z0-9_+-]+){1,3}"));
}
void exactRead(int fd, char *p, size_t n) {
    while (n) { ssize_t r = read(fd,p,n); if (r < 0 && errno == EINTR) continue;
        need(r > 0,"Incomplete request"); p += r; n -= r; }
}
std::string field(size_t maximum) {
    std::array<unsigned char,4> b{}; exactRead(0,reinterpret_cast<char*>(b.data()),4);
    size_t n = (size_t(b[0])<<24)|(size_t(b[1])<<16)|(size_t(b[2])<<8)|b[3];
    need(n > 0 && n <= maximum,"Invalid request size");
    std::string s(n,'\0'); exactRead(0,s.data(),n); need(clean(s,maximum),"Invalid request text"); return s;
}
void send(const char *message) { size_t n = strlen(message); while(n) {
    ssize_t w=write(1,message,n); if(w<0 && errno==EINTR)continue; if(w<=0)return; message+=w;n-=w;
} }
void save(const std::string &path, const std::string &value) {
    int fd=open((path+".new").c_str(),O_WRONLY|O_CREAT|O_TRUNC|O_NOFOLLOW|O_CLOEXEC,0600);
    need(fd>=0,"Cannot stage account state");
    bool ok=write(fd,value.data(),value.size())==ssize_t(value.size()) && fsync(fd)==0;
    close(fd); need(ok,"Cannot sync account state");
    need(rename((path+".new").c_str(),path.c_str())==0,"Cannot commit account state");
    int dir=open(state,O_RDONLY|O_DIRECTORY|O_CLOEXEC|O_NOFOLLOW);need(dir>=0,"Invalid state directory");
    ok=fsync(dir)==0;close(dir);need(ok,"Cannot sync state directory");
}
int run(const std::vector<std::string> &args, const std::string *input=nullptr) {
    int pipefd[2]{-1,-1}; if(input)need(pipe2(pipefd,O_CLOEXEC)==0,"Cannot create password pipe");
    pid_t pid=fork();need(pid>=0,"Cannot start account tool");
    if(pid==0) {
        int nullfd=open("/dev/null",O_RDWR);
        if(nullfd<0)_exit(126);
        dup2(input?pipefd[0]:nullfd,0);dup2(nullfd,1);dup2(nullfd,2);
        if(input){close(pipefd[0]);close(pipefd[1]);}
        if(nullfd>2)close(nullfd);
        std::vector<char*> argv;for(auto &a:args)argv.push_back(const_cast<char*>(a.c_str()));argv.push_back(nullptr);
        execv(argv[0],argv.data());_exit(127);
    }
    if(input) {
        close(pipefd[0]);size_t offset=0;while(offset<input->size()) {
            ssize_t n=write(pipefd[1],input->data()+offset,input->size()-offset);
            if(n<0 && errno==EINTR)continue;
            if(n<=0)break;
            offset+=n;
        } close(pipefd[1]);
    }
    int status=0;while(waitpid(pid,&status,0)<0){if(errno!=EINTR)return 125;}
    return WIFEXITED(status)?WEXITSTATUS(status):125;
}
int selftest() {
    for(const auto *s:{"root:evil","-root","../alice","Alice","","a\nb","a b"})if(username(s))return 1;
    for(const auto *s:{"alice","alice-1","user_2"})if(!username(s))return 1;
    for(const auto *s:{"../etc/passwd","Europe/../../etc","/etc/passwd","Europe//Paris","Europe/Paris\n"})if(validTimezone(s))return 1;
    for(const auto *s:{"Europe/Istanbul","UTC","America/Argentina/Buenos_Aires"})if(!validTimezone(s))return 1;
    if(clean(std::string("a\0b",3),32)||clean("line\n",32)||clean(std::string(129,'a'),128))return 1;
    return 0;
}
}
int main(int argc,char **argv) {
    if(argc==2 && std::string_view(argv[1])=="--self-test")return selftest();
    umask(0077);prctl(PR_SET_DUMPABLE,0);signal(SIGPIPE,SIG_IGN);
    std::string password;
    try {
        need(argc==1 && geteuid()==0,"Provisioner must be socket activated as root");
        ucred peer{};socklen_t size=sizeof(peer);
        need(getsockopt(0,SOL_SOCKET,SO_PEERCRED,&peer,&size)==0 && size==sizeof(peer),"Missing local peer");
        passwd *setup=getpwnam("uke-setup");need(setup && setup->pw_uid>0 && setup->pw_uid<1000 && peer.uid==setup->pw_uid,"Unauthorized setup peer");
        timeval timeout{30,0};setsockopt(0,SOL_SOCKET,SO_RCVTIMEO,&timeout,sizeof(timeout));
        std::string user=field(32),name=field(128);password=field(1024);
        std::string locale=field(32),zone=field(128);
        need(username(user) && name.find(':')==std::string::npos,"Invalid account name");
        need(locale=="tr_TR.UTF-8" || locale=="en_US.UTF-8","Unsupported locale");
        need(validTimezone(zone),"Invalid timezone");
        struct stat st{};need(lstat(state,&st)==0 && S_ISDIR(st.st_mode) && st.st_uid==0 && (st.st_mode&0777)==0700,"Unsafe state directory");
        std::string base=state;need(lstat((base+"/done").c_str(),&st)<0 && errno==ENOENT,"Setup already completed");
        int lock=open((base+"/lock").c_str(),O_CREAT|O_RDWR|O_NOFOLLOW|O_CLOEXEC,0600);
        need(lock>=0 && flock(lock,LOCK_EX|LOCK_NB)==0,"Another setup request is running");
        need(lstat((base+"/done").c_str(),&st)<0 && errno==ENOENT,"Setup already completed");
        // Crash recovery is restricted to the sole normal account named by our
        // root-owned journal. Never remove a user or its home on failure.
        std::string pending;
        int journal=open((base+"/pending").c_str(),O_RDONLY|O_NOFOLLOW|O_CLOEXEC);
        if(journal>=0){char buf[34]{};ssize_t n=read(journal,buf,33);close(journal);need(n>0&&n<=32,"Invalid setup journal");pending.assign(buf,n);need(username(pending),"Invalid setup journal");}
        else need(errno==ENOENT,"Cannot open setup journal");
        unsigned count=0;std::string existing;
        setpwent();while(passwd *p=getpwent())if(p->pw_uid>=1000 && p->pw_uid<65534){++count;existing=p->pw_name;}endpwent();
        need(count==0 || (count==1 && pending==user && existing==user),"Existing user prevents first-account setup");
        need(pending.empty() || pending==user,"Resume with the original account name");
        if(count==0)need(getpwnam(user.c_str())==nullptr,"Account already exists");
        need(getgrnam("wheel")!=nullptr,"Administrator group is missing");
        pwquality_settings_t *quality=pwquality_default_settings();need(quality,"Password policy unavailable");
        int config=pwquality_read_config(quality,nullptr,nullptr);
        need(config==0,"Password policy configuration is invalid");
        int minimum=12;pwquality_get_int_value(quality,PWQ_SETTING_MIN_LENGTH,&minimum);
        pwquality_set_int_value(quality,PWQ_SETTING_MIN_LENGTH,std::max(12,minimum));
        int score=pwquality_check(quality,password.c_str(),nullptr,user.c_str(),nullptr);pwquality_free_settings(quality);
        need(password.size()>=12 && score>=0,"Choose a stronger password with at least 12 characters");
        if(pending.empty())save(base+"/pending",user);
        if(count==0)need(run({"/usr/sbin/useradd","--create-home","--groups","wheel","--comment",name,"--",user})==0,"Account creation failed; retry with the same name");
        std::string line=user+":"+password+"\n";
        int status=run({"/usr/sbin/chpasswd"},&line);wipe(line);wipe(password);need(status==0,"Password policy refused; retry with the same name");
        need(run({"/usr/bin/localectl","set-locale","LANG="+locale})==0,"Locale setup failed; retry with the same name");
        need(run({"/usr/bin/timedatectl","set-timezone",zone})==0,"Timezone setup failed; retry with the same name");
        need(run({"/usr/sbin/usermod","--append","--groups","wheel",user})==0,"Administrator setup failed");
        save(base+"/done",user+"\n");send("OK\n");close(lock);return 0;
    } catch(const std::exception &e) {wipe(password);send("ERROR: ");send(e.what());send("\n");return 1;}
}
