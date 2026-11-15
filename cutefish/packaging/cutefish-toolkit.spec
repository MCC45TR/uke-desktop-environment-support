Name:           cutefish-toolkit
Version:        1.0^20261115
Release:        1%{?dist}
Summary:        Upstream Cutefish toolkit for Fedora
License:        BSD-3-Clause AND MIT
URL:            https://github.com/cutefishos/cutefish-toolkit
ExclusiveArch:  aarch64
Source0:        https://codeload.github.com/cutefishos/cutefish-toolkit/tar.gz/41782083b6926416645bbfd10d426816c24a7eae#/cutefish-toolkit-41782083b6926416645bbfd10d426816c24a7eae.tar.gz
Source100:      sources.lock.json
Source1:        https://codeload.github.com/google/skia/tar.gz/ea1e651d7a105f5ca327dfd65d28957957279e2e#/skia-ea1e651d7a105f5ca327dfd65d28957957279e2e.tar.gz
Provides:       bundled(skia) = 156
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  file
BuildRequires:  findutils
BuildRequires:  coreutils
BuildRequires:  clang
BuildRequires:  gn
BuildRequires:  python3
BuildRequires:  binutils
BuildRequires:  wayland-devel >= 1.23
BuildRequires:  wayland-protocols-devel >= 1.39
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  systemd-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libicu-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  zlib-ng-compat-devel
BuildRequires:  expat-devel
BuildRequires:  libwebp-devel
BuildRequires:  libtiff-devel
BuildRequires:  libheif-devel
BuildRequires:  libjxl-devel
Requires:       libjxl
Conflicts:      cutefish-desktop < 1.0^20261115

%description
cutefish-toolkit built from the exact upstream revision recorded in sources.lock.json.
Fedora packaging preserves upstream attribution. Installation does not enable
services or select a desktop. Hardware and graphical acceptance are separate.

%package devel
Summary:        Development headers and CMake targets
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, linker names and CMake exports for this Cutefish library.

%prep
printf '%s  %s\n' 'dfa1465ad0d4f179fbc0d4a250e6eee84b86a866936ea5e2682f86fd50005d08' '%{SOURCE0}' | sha256sum -c -
%setup -q -n cutefish-toolkit-41782083b6926416645bbfd10d426816c24a7eae
printf '%s  %s\n' 'bda98e2ab5edb8a64d513ee5a8ea1100db503c9646d223c151de9e40d0212bde' '%{SOURCE1}' | sha256sum -c -
mkdir -p third_party/skia
tar -xf %{SOURCE1} --strip-components=1 -C third_party/skia
ln -sf /usr/bin/gn third_party/skia/bin/gn

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
awk '$0 ~ /^\/usr\/include\// || $0 ~ /\/cmake\// || $0 ~ /\/libcutefish-[^/]*[.]so$/ {print > "devel.files"; next} {print > "runtime.files"}' all.files
# Configuration belongs to RPM and must survive supported upgrades.
sed -i 's|^/etc/|%config(noreplace) /etc/|' runtime.files

%check
! find %{buildroot} -type f \( -name '*.py' -o -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) | grep . || exit 1
! grep -rlE '^#!.*python' %{buildroot} || exit 1
test ! -d %{buildroot}%{_datadir}/backgrounds/cutefishos

%files -f runtime.files
%license LICENSES

%files devel -f devel.files

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-1
- Split the pinned nightly source into an independently built Fedora RPM.
