// SPDX-License-Identifier: BSD-3-Clause
#include <QApplication>
#include <QComboBox>
#include <QCloseEvent>
#include <QFormLayout>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QLocalSocket>
#include <QMessageBox>
#include <QPushButton>
#include <QScrollArea>
#include <QTimer>
#include <QVBoxLayout>
#include <QWidget>
#include <array>
#include <sys/prctl.h>

class SetupWindow : public QWidget { void closeEvent(QCloseEvent *event) override { event->ignore(); } };

int main(int argc,char **argv) {
    prctl(PR_SET_DUMPABLE,0);
    QApplication app(argc,argv);SetupWindow window;window.setWindowTitle("Cutefish · First account");
    app.setStyleSheet("QWidget { font-family: Inter, 'Noto Sans'; font-size: 18px; background: #f6f7fb; color: #202637; } QLineEdit, QComboBox { background: white; border: 1px solid #b7c0d7; border-radius: 8px; padding: 10px; } QPushButton { background: #dde7fc; border: 1px solid #b7c9eb; border-radius: 8px; padding: 12px; min-height: 24px; } QPushButton:pressed { background: #a8c6ff; }");
    auto *layout=new QVBoxLayout(&window);auto *title=new QLabel("Welcome to Cutefish");
    title->setStyleSheet("font-size: 30px; font-weight: 600;");layout->addWidget(title);
    layout->addWidget(new QLabel("Create your administrator account. Use at least 12 characters for the password."));
    auto *form=new QFormLayout;layout->addLayout(form);
    QLineEdit user,name,password,confirmation;user.setMaxLength(32);name.setMaxLength(128);
    password.setMaxLength(256);confirmation.setMaxLength(256);
    password.setEchoMode(QLineEdit::Password);confirmation.setEchoMode(QLineEdit::Password);
    std::array<QLineEdit*,4> fields{&user,&name,&password,&confirmation};
    for(auto *field:fields)field->setMinimumHeight(36);
    form->addRow("Username",&user);form->addRow("Full name",&name);form->addRow("Password",&password);form->addRow("Repeat password",&confirmation);
    QComboBox locale,zone;locale.addItem("Türkçe","tr_TR.UTF-8");locale.addItem("English","en_US.UTF-8");
    for(const auto *value:{"Europe/Istanbul","UTC","Europe/London","Europe/Berlin","Europe/Paris","America/New_York","America/Los_Angeles","Asia/Tokyo"})zone.addItem(value,value);
    form->addRow("Language",&locale);form->addRow("Timezone",&zone);
    QLabel status;status.setWordWrap(true);layout->addWidget(&status);
    // An in-process touch keyboard works before any input-method service has
    // an account or session. It never sends privileged compositor commands.
    auto *keyboard=new QGridLayout;layout->addLayout(keyboard);QLineEdit *focused=&user;
    QObject::connect(&app,&QApplication::focusChanged,&window,[&](QWidget*,QWidget *now){for(auto *field:fields)if(now==field)focused=field;});
    bool shift=false;
    const std::array<QString,4> rows{"1234567890", "qwertyuiopğü", "asdfghjklşi", "zxcvbnmöç"};
    for(int r=0;r<int(rows.size());++r)for(int c=0;c<rows[r].size();++c){
        QString letter=rows[r].mid(c,1);auto *key=new QPushButton(letter);key->setFocusPolicy(Qt::NoFocus);keyboard->addWidget(key,r,c);
        QObject::connect(key,&QPushButton::clicked,&window,[&,letter]{focused->insert(shift?letter.toUpper():letter);});
    }
    auto *caps=new QPushButton("Shift");caps->setCheckable(true);caps->setFocusPolicy(Qt::NoFocus);keyboard->addWidget(caps,4,0,1,2);
    QObject::connect(caps,&QPushButton::toggled,&window,[&](bool value){shift=value;});
    auto *space=new QPushButton("Space");space->setFocusPolicy(Qt::NoFocus);keyboard->addWidget(space,4,2,1,5);
    QObject::connect(space,&QPushButton::clicked,&window,[&]{focused->insert(" ");});
    auto *back=new QPushButton("⌫");back->setFocusPolicy(Qt::NoFocus);keyboard->addWidget(back,4,7,1,2);
    QObject::connect(back,&QPushButton::clicked,&window,[&]{focused->backspace();});
    auto *next=new QPushButton("Next field");next->setFocusPolicy(Qt::NoFocus);keyboard->addWidget(next,4,9,1,3);
    QObject::connect(next,&QPushButton::clicked,&window,[&]{for(size_t i=0;i<fields.size();++i)if(focused==fields[i]){fields[(i+1)%fields.size()]->setFocus();break;}});
    QPushButton create("Create account and continue");layout->addWidget(&create);
    QLocalSocket socket;QByteArray response;
    QObject::connect(&create,&QPushButton::clicked,&window,[&]{
        if(password.text()!=confirmation.text()){status.setText("The passwords do not match.");return;}
        if(user.text().isEmpty()||name.text().isEmpty()||password.text().size()<12){status.setText("Complete every field and use a password with at least 12 characters.");return;}
        create.setEnabled(false);status.setText("Creating your account…");response.clear();
        socket.connectToServer("/run/uke-cutefish-firstboot.sock");
    });
    QObject::connect(&socket,&QLocalSocket::connected,&window,[&]{
        for(const QString &value:{user.text(),name.text(),password.text(),locale.currentData().toString(),zone.currentData().toString()}){
            QByteArray bytes=value.toUtf8();quint32 n=bytes.size();char header[]{char(n>>24),char(n>>16),char(n>>8),char(n)};
            socket.write(header,4);socket.write(bytes);bytes.fill('\0');
        }
        socket.flush();password.clear();confirmation.clear();
    });
    QObject::connect(&socket,&QLocalSocket::readyRead,&window,[&]{
        response+=socket.readAll();if(response.size()>2048){socket.abort();status.setText("Invalid response from account setup.");return;}
        if(response.contains('\n')){
            if(response=="OK\n"){status.setText("Your account is ready. Opening the Cutefish login screen…");QTimer::singleShot(1000,&app,&QApplication::quit);}
            else{status.setText(QString::fromUtf8(response));socket.disconnectFromServer();create.setEnabled(true);}
        }
    });
    QObject::connect(&socket,&QLocalSocket::errorOccurred,&window,[&](QLocalSocket::LocalSocketError){status.setText("Account setup is unavailable. Keep this screen open and retry.");create.setEnabled(true);});
    window.resize(1000,850);window.showFullScreen();user.setFocus();return app.exec();
}
