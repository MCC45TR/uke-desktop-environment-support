Name:           cutefish-dm
Version:        1.0^20261115
Release:        1%{?dist}
Summary:        Upstream Cutefish dm for Fedora
License:        BSD-3-Clause
URL:            https://github.com/cutefishos/cutefish-dm
ExclusiveArch:  aarch64
Source0:        https://codeload.github.com/cutefishos/cutefish-dm/tar.gz/2d06f21aba761b6846c8e10170f5da01addbc8a6#/cutefish-dm-2d06f21aba761b6846c8e10170f5da01addbc8a6.tar.gz
Source100:      sources.lock.json
Source1:        cutefish-dm
Source2:        cutefish-dm-greeter
Source3:        cutefish-greeter.conf
Requires(pre):  /usr/bin/systemd-sysusers
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  file
BuildRequires:  findutils
BuildRequires:  coreutils
BuildRequires:  cutefish-toolkit-devel >= 1.0^20261115
BuildRequires:  pam-devel
BuildRequires:  systemd-rpm-macros
Requires:       cutefish-compositor >= 1.0^20261115
Requires:       systemd
Requires:       pam
Requires:       gnome-keyring-pam
Conflicts:      cutefish-desktop < 1.0^20261115

%description
cutefish-dm built from the exact upstream revision recorded in sources.lock.json.
Fedora packaging preserves upstream attribution. Installation does not enable
services or select a desktop. Hardware and graphical acceptance are separate.

%prep
printf '%s  %s\n' 'b6c8436eb840d2770b754feef75126e848b24f6736c5e5da8af410302f089281' '%{SOURCE0}' | sha256sum -c -
%setup -q -n cutefish-dm-2d06f21aba761b6846c8e10170f5da01addbc8a6

%build
%cmake -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/cutefish-dm
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/cutefish-dm-greeter
install -Dm644 %{SOURCE3} %{buildroot}%{_sysusersdir}/cutefish-greeter.conf
install -d -m700 %{buildroot}%{_localstatedir}/lib/cutefish-greeter
install -Dm644 %{SOURCE100} %{buildroot}%{_docdir}/%{name}/sources.lock.json
# Retain every source-tree license and bundled-library notice with its path.
mkdir LICENSES
find . -type f \( -iname 'license*' -o -iname 'copying*' -o -iname 'notice*' \) ! -path './LICENSES/*' ! -path './%{_vpath_builddir}/*' -print0 | while IFS= read -r -d '' path; do
    install -Dm644 "$path" "LICENSES/${path#./}"
done
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > all.files
cp all.files runtime.files
# Configuration belongs to RPM and must survive supported upgrades.
sed -i 's|^/etc/|%config(noreplace) /etc/|' runtime.files

%check
! find %{buildroot} -type f \( -name '*.py' -o -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) | grep . || exit 1
! grep -rlE '^#!.*python' %{buildroot} || exit 1
test ! -d %{buildroot}%{_datadir}/backgrounds/cutefishos
! grep -E 'common-auth|common-account' %{buildroot}%{_sysconfdir}/pam.d/cutefish-dm* || exit 1

%files -f runtime.files
%license LICENSES
%attr(0700,cutefish-greeter,cutefish-greeter) %dir %{_localstatedir}/lib/cutefish-greeter

%pre
systemd-sysusers %{_sysusersdir}/cutefish-greeter.conf 2>/dev/null || systemd-sysusers - <<'EOF'
u cutefish-greeter - "Cutefish display manager" /var/lib/cutefish-greeter /usr/sbin/nologin
EOF

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-1
- Split the pinned nightly source into an independently built Fedora RPM.
