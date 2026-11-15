Name:           cutefish-calendar
Version:        1.0^20261115
Release:        2%{?dist}
Summary:        Upstream Cutefish calendar for Fedora
License:        BSD-3-Clause
URL:            https://github.com/cutefishos/calendar
ExclusiveArch:  aarch64
Source0:        https://codeload.github.com/cutefishos/calendar/tar.gz/4332987418637a78d3d302159ec74bb5de57d4e2#/calendar-4332987418637a78d3d302159ec74bb5de57d4e2.tar.gz
Source100:      sources.lock.json
Patch0:         calendar-libical4.patch
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  file
BuildRequires:  findutils
BuildRequires:  coreutils
BuildRequires:  cutefish-toolkit-devel >= 1.0^20261115
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libical) >= 4.0.0
BuildRequires:  gtest-devel tzdata
BuildRequires:  pkgconfig(libsystemd)
Requires:       cutefish-toolkit >= 1.0^20261115
Conflicts:      cutefish-desktop < 1.0^20261115

%description
cutefish-calendar built from the exact upstream revision recorded in sources.lock.json.
Fedora packaging preserves upstream attribution. Installation does not enable
services or select a desktop. Hardware and graphical acceptance are separate.

%prep
printf '%s  %s\n' '33c51dc8b01e9aec4c9121e583f5760f99a1528f0743502fc70cd9563c91aecb' '%{SOURCE0}' | sha256sum -c -
%setup -q -n calendar-4332987418637a78d3d302159ec74bb5de57d4e2

%patch -P 0 -p1

%build
%cmake -DBUILD_TESTING=ON
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
%{_vpath_builddir}/tests/calendar-core-tests
! find %{buildroot} -type f \( -name '*.py' -o -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) | grep . || exit 1
! grep -rlE '^#!.*python' %{buildroot} || exit 1
test ! -d %{buildroot}%{_datadir}/backgrounds/cutefishos

%files -f runtime.files
%license LICENSES

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-2
- Adapt recurrence ownership and duration access to original Fedora libical 4.
- Run the upstream calendar core tests, including recurrence editing.

* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-1
- Split the pinned nightly source into an independently built Fedora RPM.
