Name:           xdg-desktop-portal-cutefish
Version:        1.0^20261115
Release:        1%{?dist}
Summary:        Upstream Cutefish xdg-desktop-portal-cutefish for Fedora
License:        BSD-3-Clause
URL:            https://github.com/cutefishos/xdg-desktop-portal-cutefish
ExclusiveArch:  aarch64
Source0:        https://codeload.github.com/cutefishos/xdg-desktop-portal-cutefish/tar.gz/19765bcce46880e36a8cfb6b7bdcc6bd09076b59#/xdg-desktop-portal-cutefish-19765bcce46880e36a8cfb6b7bdcc6bd09076b59.tar.gz
Source100:      sources.lock.json
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  file
BuildRequires:  findutils
BuildRequires:  coreutils
BuildRequires:  cutefish-toolkit-devel >= 1.0^20261115
BuildRequires:  pkgconfig(libsystemd)
Requires:       xdg-desktop-portal
Conflicts:      cutefish-desktop < 1.0^20261115

BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(wayland-protocols)

%description
xdg-desktop-portal-cutefish built from the exact upstream revision recorded in sources.lock.json.
Fedora packaging preserves upstream attribution. Installation does not enable
services or select a desktop. Hardware and graphical acceptance are separate.

%prep
printf '%s  %s\n' '7b6d0e71eced658705df58369852245e47abfa5967698e54ff9e0ed1368cc0a0' '%{SOURCE0}' | sha256sum -c -
%setup -q -n xdg-desktop-portal-cutefish-19765bcce46880e36a8cfb6b7bdcc6bd09076b59

%build
%cmake -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
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
