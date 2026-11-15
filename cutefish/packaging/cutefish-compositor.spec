Name:           cutefish-compositor
Version:        1.0^20261115
Release:        1%{?dist}
Summary:        Upstream Cutefish compositor for Fedora
License:        BSD-3-Clause AND MIT
URL:            https://github.com/cutefishos/cutefish-compositor
ExclusiveArch:  aarch64
Source0:        https://codeload.github.com/cutefishos/cutefish-compositor/tar.gz/1d3b480db10a1317c4591ed10684848896a441e1#/cutefish-compositor-1d3b480db10a1317c4591ed10684848896a441e1.tar.gz
Source100:      sources.lock.json
Source1:        cutefish-auth
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  file
BuildRequires:  findutils
BuildRequires:  coreutils
BuildRequires:  cutefish-toolkit-devel >= 1.0^20261115
BuildRequires:  cutefish-framework-devel >= 1.0^20261115
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pam-devel
Requires:       cutefish-core >= 1.0^20261115
Requires:       cutefish-framework >= 1.0^20261115
Requires:       cutefish-icon-theme >= 1.0^20261115
Requires:       xorg-x11-server-Xwayland
Requires:       polkit
Requires:       pam
Conflicts:      cutefish-desktop < 1.0^20261115

%description
cutefish-compositor built from the exact upstream revision recorded in sources.lock.json.
Fedora packaging preserves upstream attribution. Installation does not enable
services or select a desktop. Hardware and graphical acceptance are separate.

%prep
printf '%s  %s\n' '6f396436cf3360fac874efe2f9cd5998e4741911c0d82a902df580063ba8593c' '%{SOURCE0}' | sha256sum -c -
%setup -q -n cutefish-compositor-1d3b480db10a1317c4591ed10684848896a441e1

%build
%cmake -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/cutefish-auth
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

%files -f runtime.files
%license LICENSES

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-1
- Split the pinned nightly source into an independently built Fedora RPM.
