Name:           uke-cutefish-firstboot
Version:        1.0.0
Release:        2%{?dist}
Summary:        Credentials-free first-account setup for the Uke Cutefish image
License:        BSD-3-Clause
URL:            https://github.com/MCC45TR/uke-desktop-environment-support
ExclusiveArch:  aarch64
Source0:        backend.cpp
Source1:        frontend.cpp
Source2:        CMakeLists.txt
Source3:        LICENSE
Source4:        uke-cutefish-firstboot.socket
Source5:        uke-cutefish-firstboot-backend@.service
Source6:        uke-cutefish-firstboot.service
Source7:        firstboot-session.sh
Source8:        firstboot-display.sh
Source9:        firstboot-sysusers.conf
Source10:       firstboot-tmpfiles.conf
Source11:       dm-firstboot.conf
BuildRequires:  gcc-c++ cmake ninja-build qt6-qtbase-devel pkgconfig(pwquality)
BuildRequires:  systemd-rpm-macros
Requires:       cutefish-dm >= 1.0^20261115
Requires:       cutefish-compositor >= 1.0^20261115
Requires:       dbus-daemon shadow-utils systemd systemd-pam libpwquality qt6-qtwayland
Requires(pre):  /usr/bin/systemd-sysusers

%description
A dedicated unprivileged graphical setup session with an on-screen keyboard.
A socket-activated root helper accepts only the setup account, creates the first
password-protected wheel account and commits completion after all tools succeed.
The display manager waits for setup. No default human account is installed.
Graphical, PAM/SELinux and physical tablet acceptance remain separate tests.

%prep
%setup -q -c -T
cp %{SOURCE0} backend.cpp
cp %{SOURCE1} frontend.cpp
cp %{SOURCE2} CMakeLists.txt
cp %{SOURCE3} LICENSE

%build
%cmake
%cmake_build

%install
%cmake_install
install -Dm644 %{SOURCE4} %{buildroot}%{_unitdir}/uke-cutefish-firstboot.socket
install -Dm644 %{SOURCE5} %{buildroot}%{_unitdir}/uke-cutefish-firstboot@.service
install -Dm644 %{SOURCE6} %{buildroot}%{_unitdir}/uke-cutefish-firstboot.service
install -Dm755 %{SOURCE7} %{buildroot}%{_libexecdir}/uke-cutefish-firstboot-session
install -Dm755 %{SOURCE8} %{buildroot}%{_libexecdir}/uke-cutefish-firstboot-display
install -Dm644 %{SOURCE9} %{buildroot}%{_sysusersdir}/uke-cutefish-firstboot.conf
install -Dm644 %{SOURCE10} %{buildroot}%{_tmpfilesdir}/uke-cutefish-firstboot.conf
install -Dm644 %{SOURCE11} %{buildroot}%{_unitdir}/cutefish-dm.service.d/10-uke-firstboot.conf
install -d -m700 %{buildroot}%{_localstatedir}/lib/uke-cutefish-firstboot
install -d -m700 %{buildroot}%{_localstatedir}/lib/uke-cutefish-setup

%check
%ctest

%pre
systemd-sysusers - <<'SYSUSERS'
u uke-setup - "Uke first-account setup" /var/lib/uke-cutefish-setup /usr/sbin/nologin
SYSUSERS

%files
%license LICENSE
%{_libexecdir}/uke-cutefish-firstboot*
%{_unitdir}/uke-cutefish-firstboot*
%{_unitdir}/cutefish-dm.service.d/10-uke-firstboot.conf
%{_sysusersdir}/uke-cutefish-firstboot.conf
%{_tmpfilesdir}/uke-cutefish-firstboot.conf
%attr(0700,root,root) %dir %{_localstatedir}/lib/uke-cutefish-firstboot
%attr(0700,uke-setup,uke-setup) %dir %{_localstatedir}/lib/uke-cutefish-setup

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0.0-2
- Avoid the libc timezone symbol and require the original Fedora Wayland plugin.

* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0.0-1
- Add a dedicated first-account session and narrowly scoped provisioner.
