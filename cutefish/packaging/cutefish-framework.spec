Name:           cutefish-framework
Version:        1.0^20261115
Release:        2%{?dist}
Summary:        Upstream Cutefish framework for Fedora
License:        BSD-3-Clause AND Apache-2.0 WITH LLVM-exception AND BSL-1.0 AND MIT AND BSD-2-Clause AND FTL
URL:            https://github.com/cutefishos/cutefish-framework
ExclusiveArch:  aarch64
Source0:        https://codeload.github.com/cutefishos/cutefish-framework/tar.gz/15174d3b9d76132dc5ffd82794f1f1cd617be8f2#/cutefish-framework-15174d3b9d76132dc5ffd82794f1f1cd617be8f2.tar.gz
Source100:      sources.lock.json
Source1:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/constants.tar.gz#/pdfium-constants-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source2:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/core.tar.gz#/pdfium-core-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source3:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/fpdfsdk.tar.gz#/pdfium-fpdfsdk-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source4:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/fxjs.tar.gz#/pdfium-fxjs-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source5:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/public.tar.gz#/pdfium-public-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source6:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/third_party/agg23.tar.gz#/pdfium-third_party-agg23-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source7:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/third_party/bigint.tar.gz#/pdfium-third_party-bigint-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source8:        https://pdfium.googlesource.com/pdfium/+archive/99da130a26ad610843d041a509efd8ea68cc05b7/third_party/freetype.tar.gz#/pdfium-third_party-freetype-99da130a26ad610843d041a509efd8ea68cc05b7.tar.gz
Source9:        https://pdfium.googlesource.com/pdfium/+/99da130a26ad610843d041a509efd8ea68cc05b7/LICENSE?format=TEXT#/pdfium-license-99da130a26ad610843d041a509efd8ea68cc05b7.b64
Source10:        https://pdfium.googlesource.com/pdfium/+/99da130a26ad610843d041a509efd8ea68cc05b7/DEPS?format=TEXT#/pdfium-deps-99da130a26ad610843d041a509efd8ea68cc05b7.b64
Source11:        https://chromium.googlesource.com/chromium/src/build/+/0c62137b8623a3fab2c6aa5d7c94f719b3aa31f6/build_config.h?format=TEXT#/chromium-build_config.h-0c62137b8623a3fab2c6aa5d7c94f719b3aa31f6.b64
Source12:        https://chromium.googlesource.com/chromium/src/build/+/0c62137b8623a3fab2c6aa5d7c94f719b3aa31f6/buildflag.h?format=TEXT#/chromium-buildflag.h-0c62137b8623a3fab2c6aa5d7c94f719b3aa31f6.b64
Source13:        https://chromium.googlesource.com/external/github.com/jk-jeon/dragonbox/+archive/beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44/include.tar.gz#/dragonbox-beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44.tar.gz
Source14:        https://chromium.googlesource.com/external/github.com/jk-jeon/dragonbox/+/beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44/LICENSE-Apache2-LLVM?format=TEXT#/dragonbox-license-apache2-llvm-beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44.b64
Source15:        https://chromium.googlesource.com/external/github.com/jk-jeon/dragonbox/+/beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44/LICENSE-Boost?format=TEXT#/dragonbox-license-boost-beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44.b64
Source16:        https://chromium.googlesource.com/external/github.com/fastfloat/fast_float/+archive/42f254836ee416ffcf2f4e6576260003ac33d48c/include.tar.gz#/fast_float-42f254836ee416ffcf2f4e6576260003ac33d48c.tar.gz
Source17:        https://chromium.googlesource.com/external/github.com/fastfloat/fast_float/+/42f254836ee416ffcf2f4e6576260003ac33d48c/LICENSE-APACHE?format=TEXT#/fast_float-license-apache-42f254836ee416ffcf2f4e6576260003ac33d48c.b64
Source18:        https://chromium.googlesource.com/external/github.com/fastfloat/fast_float/+/42f254836ee416ffcf2f4e6576260003ac33d48c/LICENSE-BOOST?format=TEXT#/fast_float-license-boost-42f254836ee416ffcf2f4e6576260003ac33d48c.b64
Source19:        https://chromium.googlesource.com/external/github.com/fastfloat/fast_float/+/42f254836ee416ffcf2f4e6576260003ac33d48c/LICENSE-MIT?format=TEXT#/fast_float-license-mit-42f254836ee416ffcf2f4e6576260003ac33d48c.b64
Provides:       bundled(pdfium) = 8158
Provides:       bundled(dragonbox) = 1
Provides:       bundled(fast_float) = 8

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  file
BuildRequires:  findutils
BuildRequires:  coreutils
BuildRequires:  cutefish-toolkit-devel >= 1.0^20261115
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(harfbuzz-subset)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libhwy)
BuildRequires:  pkgconfig(absl_flat_hash_set)
BuildRequires:  pkgconfig(absl_inlined_vector)
BuildRequires:  pkgconfig(absl_cleanup)
BuildRequires:  pkgconfig(zlib)
Requires:       cutefish-toolkit >= 1.0^20261115
Requires:       NetworkManager
Requires:       bluez
Requires:       upower
Requires:       pipewire
Requires:       pipewire-pulseaudio
Requires:       wireplumber
Requires:       gnome-keyring
Requires:       gnome-keyring-pam
Conflicts:      cutefish-desktop < 1.0^20261115

%description
cutefish-framework built from the exact upstream revision recorded in sources.lock.json.
Fedora packaging preserves upstream attribution. Installation does not enable
services or select a desktop. Hardware and graphical acceptance are separate.

%package devel
Summary:        Development headers and CMake targets
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cutefish-toolkit-devel >= 1.0^20261115
Requires:       pkgconfig(libpipewire-0.3) >= 0.3.65

%description devel
Headers, linker names and CMake exports for this Cutefish library.

%prep
printf '%s  %s\n' '8ae50beca769c5350e447ef8cf4a554d5e96ce699709c253f7f23b05e11badf4' '%{SOURCE0}' | sha256sum -c -
%setup -q -n cutefish-framework-15174d3b9d76132dc5ffd82794f1f1cd617be8f2

printf '%s  %s\n' 'cf8f69a6e1584b9627a69f364aeb4f70d15a4770d025d88f207c0150e7287338' '%{SOURCE1}' | sha256sum -c -
mkdir -p third_party/pdfium/constants
tar -xf %{SOURCE1} -C third_party/pdfium/constants
printf '%s  %s\n' '12a18f2adc09ad601e0de32fe73f6bc1ec09f29c6f751c75bdfbb70f38b78d15' '%{SOURCE2}' | sha256sum -c -
mkdir -p third_party/pdfium/core
tar -xf %{SOURCE2} -C third_party/pdfium/core
printf '%s  %s\n' '7783a277884384808c7076b389868eaf641554b36adda53aa5f1ce0b273e45ff' '%{SOURCE3}' | sha256sum -c -
mkdir -p third_party/pdfium/fpdfsdk
tar -xf %{SOURCE3} -C third_party/pdfium/fpdfsdk
printf '%s  %s\n' 'f022408b6ab743aeeced20f1dcc5e0b079575b342b3a59e878917c2036d7581b' '%{SOURCE4}' | sha256sum -c -
mkdir -p third_party/pdfium/fxjs
tar -xf %{SOURCE4} -C third_party/pdfium/fxjs
printf '%s  %s\n' '38595faa106aefbb4b1cc17b0ddb1cfc57321ef2545762f6a3dc347ca4206fde' '%{SOURCE5}' | sha256sum -c -
mkdir -p third_party/pdfium/public
tar -xf %{SOURCE5} -C third_party/pdfium/public
printf '%s  %s\n' '447333d95850ab30fc18b79fce615f6b4c40cc2a093d2f8f45d205e19156d8c1' '%{SOURCE6}' | sha256sum -c -
mkdir -p third_party/pdfium/third_party/agg23
tar -xf %{SOURCE6} -C third_party/pdfium/third_party/agg23
printf '%s  %s\n' '27e71572ddb03c19e116815bdaca336e868e984df0403d34e7794a4ab8c1d174' '%{SOURCE7}' | sha256sum -c -
mkdir -p third_party/pdfium/third_party/bigint
tar -xf %{SOURCE7} -C third_party/pdfium/third_party/bigint
printf '%s  %s\n' '7abe9dde901275dd13d17acf782fdf1caf3d459115b21d5ee3a12b17e4bf7b1c' '%{SOURCE8}' | sha256sum -c -
mkdir -p third_party/pdfium/third_party/freetype
tar -xf %{SOURCE8} -C third_party/pdfium/third_party/freetype
printf '%s  %s\n' 'beef23306e826b0397db1298cd6c927dcb7f912c5c162358e48151a56e492040' '%{SOURCE9}' | sha256sum -c -
mkdir -p third_party/pdfium
base64 -d %{SOURCE9} > third_party/pdfium/LICENSE
printf '%s  %s\n' 'a53ac655d8c88ddaf8d61d210a89090b6754a46c359cecda9ee447b64173f704' '%{SOURCE10}' | sha256sum -c -
mkdir -p third_party/pdfium
base64 -d %{SOURCE10} > third_party/pdfium/DEPS
printf '%s  %s\n' 'b128d29784d861ee399ba733a923884dfaf6edd254dca28e96424ec197c0c597' '%{SOURCE11}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/build
base64 -d %{SOURCE11} > third_party/pdfium-deps/build/build_config.h
printf '%s  %s\n' '77fbc9848b29919e76a154ae9cf2b7915bf4683ca942d16b43e43a7f9d1f007e' '%{SOURCE12}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/build
base64 -d %{SOURCE12} > third_party/pdfium-deps/build/buildflag.h
printf '%s  %s\n' '265f7b9eca6834e1ccfbf6f0dc3082bec73fd597c762a5df85f82a2a7f20b67c' '%{SOURCE13}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/dragonbox/include
tar -xf %{SOURCE13} -C third_party/pdfium-deps/dragonbox/include
printf '%s  %s\n' 'c71962c081584c01a7c18adb3a19137cb831604941bd829dc78751e85862dc1d' '%{SOURCE14}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/dragonbox
base64 -d %{SOURCE14} > third_party/pdfium-deps/dragonbox/LICENSE-Apache2-LLVM
printf '%s  %s\n' '5624d76e1b4569cebba65ba1f7eda5fbd231bc5ee5e4136211561b2109e0c4f8' '%{SOURCE15}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/dragonbox
base64 -d %{SOURCE15} > third_party/pdfium-deps/dragonbox/LICENSE-Boost
printf '%s  %s\n' 'd41f32edf11732748b428cbd97554b54a4ea308a8ca1a9ce56409e4c098c3506' '%{SOURCE16}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/fast_float/include
tar -xf %{SOURCE16} -C third_party/pdfium-deps/fast_float/include
printf '%s  %s\n' 'a30d4e911a93dc7d5aa52153d955f4d7fdb978d7e8977e35df3b4ea57c4dd2fc' '%{SOURCE17}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/fast_float
base64 -d %{SOURCE17} > third_party/pdfium-deps/fast_float/LICENSE-APACHE
printf '%s  %s\n' 'bbc5ffda135f303d12647a63fb37c7fa6b436335f0ce66c7d930de588d67e97c' '%{SOURCE18}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/fast_float
base64 -d %{SOURCE18} > third_party/pdfium-deps/fast_float/LICENSE-BOOST
printf '%s  %s\n' 'e284774d6f1f4d9bb73db1652e956a2c9311f6b4fcaf23e3a5735a55174cccb3' '%{SOURCE19}' | sha256sum -c -
mkdir -p third_party/pdfium-deps/fast_float
base64 -d %{SOURCE19} > third_party/pdfium-deps/fast_float/LICENSE-MIT

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
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-2
- Normalize request-time Gitiles archive headers while sealing all source bytes.

* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-1
- Split the pinned nightly source into an independently built Fedora RPM.
