# Candidate for mcc45tr/kdenext: native fedora-rawhide-aarch64 build.
# Unbuilt/unvalidated: see BUILD-PLAN.md. Never runs kosctl or enables services.
%global commit 2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5
Name:           nextkde
Version:        0.1.1
Release:        1%{?dist}
Summary:        Quickshell desktop shell for KDE Plasma Wayland
License:        GPL-3.0-only AND GPL-2.0-or-later AND MIT AND BSD-3-Clause AND Apache-2.0
URL:            https://github.com/NextKde/NextKde
# Reproducible git archive of the exact commit; see BUILD-PLAN.md.
Source0:        NextKde-%{commit}.tar.gz
Source1:        nextkde-go-vendor.tar.gz
Source2:        nextkde-licenses.txt
Source3:        Apache-2.0.txt
Source4:        GPL-2.0.txt
ExclusiveArch:  aarch64
BuildRequires:  cmake >= 3.21
BuildRequires:  qt6-rpm-macros
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  golang >= 1.26
BuildRequires:  extra-cmake-modules
BuildRequires:  gettext
BuildRequires:  python3
BuildRequires:  desktop-file-utils
BuildRequires:  qt6-qtbase-devel >= 6.6
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  kf6-kwindowsystem-devel
BuildRequires:  kf6-kiconthemes-devel
BuildRequires:  kf6-kglobalaccel-devel
BuildRequires:  kf6-kio-devel
BuildRequires:  kf6-kconfig-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kguiaddons-devel
BuildRequires:  kf6-kcmutils-devel
BuildRequires:  kf6-kcoreaddons-devel
BuildRequires:  libplasma-devel
BuildRequires:  kdecoration-devel
BuildRequires:  kwin-devel >= 6.6
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libepoxy-devel
BuildRequires:  vulkan-headers
BuildRequires:  vulkan-loader-devel
BuildRequires:  zlib-devel
BuildRequires:  libxcb-devel
Requires:       quickshell >= 0.3
Requires:       quickshell < 0.4
Requires:       kwin%{?_isa} >= 6.6
Requires:       plasma-workspace
Requires:       qt6-qtdeclarative
Requires:       qt6-qt5compat
Requires:       qt6-qtsvg
Requires:       qt6-qtimageformats
Requires:       qt6-qtwayland
Requires:       systemd
Requires:       NetworkManager
Requires:       bluez
Requires:       pipewire-pulseaudio
Requires:       pulseaudio-utils
Requires:       wl-clipboard
Requires:       cliphist
Recommends:     brightnessctl
Recommends:     kscreen
Provides:       bundled(golang(github.com/fsnotify/fsnotify)) = 1.10.1
Provides:       bundled(golang(golang.org/x/sys)) = 0.13.0

%description
NextKDE's core shell, Settings, platform and data services, KWin effects and
window decoration. Requires an existing Plasma Wayland session. No service
is enabled and no user configuration is changed on installation. Optional
apps, spatial/ONNX depth processing, ListenFree and SDKs are not included.
This experimental Rawhide/aarch64 package still needs runtime acceptance.

%prep
%setup -q -n NextKde-%{commit}
tar -xf %{SOURCE1} -C services/data-service
mkdir -p licenses
cp LICENSE licenses/NextKDE-GPL-3.0
cp kwin/glass-effect/LICENSE licenses/Glass-GPL-3.0
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} licenses/
cp shared/qml/wallpapers/vendor/flow/LICENSE licenses/Flow-MIT
cp shared/qml/wallpapers/vendor/black-hole/LICENSE licenses/BlackHole-BSD-3-Clause
cp services/data-service/vendor/github.com/fsnotify/fsnotify/LICENSE licenses/fsnotify-BSD-3-Clause
cp services/data-service/vendor/golang.org/x/sys/LICENSE licenses/x-sys-BSD-3-Clause
cp services/data-service/vendor/golang.org/x/sys/PATENTS licenses/x-sys-PATENTS
# Preserve SurfaceShape's complete MIT permission/copyright text.
cp shell/native/surface-shape/kos-surface-shape-v1.xml licenses/SurfaceShape-protocol.xml
# Use immutable installed paths for Settings fallback and IPC. Never depend on
# a deleted RPM build directory, and never modify the user's config tree.
sed -i 's|SETTINGS_QML_DIR="${CMAKE_CURRENT_SOURCE_DIR}"|SETTINGS_QML_DIR="/usr/share/kos/settings"|; s|SETTINGS_SHELL_DIR="${CMAKE_CURRENT_SOURCE_DIR}/../../shell"|SETTINGS_SHELL_DIR="/usr/share/nextkde/shell"|' apps/settings/CMakeLists.txt

%build
# Build entirely offline. A missing vendored dependency is a hard failure.
export GOPROXY=off GOSUMDB=off GOTOOLCHAIN=local GOFLAGS=-mod=vendor
export GOCACHE="$PWD/.go-cache"
%cmake -G Ninja -DBUILD_TESTING=OFF \
    -DKOS_BUILD_PLATFORM=ON -DKOS_BUILD_KWIN_PLUGINS=ON \
    -DKOS_BUILD_SPATIAL=OFF -DKOS_BUILD_CALENDAR=OFF -DKOS_BUILD_TODO=OFF \
    -DKOS_BUILD_WEATHER=OFF -DKOS_BUILD_CALCULATOR=OFF \
    -DKOS_BUILD_MUSIC=OFF -DKOS_BUILD_LISTENFREE=OFF \
    -DKDE_INSTALL_USE_QT_SYS_PATHS=ON -DFETCHCONTENT_FULLY_DISCONNECTED=ON
%cmake_build
# Glass is deliberately a separate CMake project in this upstream release.
cmake -S kwin/glass-effect -B glass-build -G Ninja \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
    -DGLASS_WAYLAND=ON -DGLASS_X11=OFF -DBUILD_TESTING=OFF
cmake --build glass-build --parallel %{_smp_build_ncpus}
# The core top-level CMake omits this service unless Weather/tests are ON.
(cd services/data-service && go build -trimpath -buildvcs=false -o kos-data-service .)

%install
%cmake_install
DESTDIR=%{buildroot} cmake --install glass-build
install -Dpm0755 services/data-service/kos-data-service %{buildroot}%{_libexecdir}/kos-data-service
# Materialize source symlinks while source relatives still exist.
mkdir -p %{buildroot}%{_datadir}/nextkde %{buildroot}%{_datadir}/shared
cp -rL shell %{buildroot}%{_datadir}/nextkde/
cp -rL shared/qml %{buildroot}%{_datadir}/shared/
# Shell's shared imports need the same complete runtime tree as Settings.
mkdir -p %{buildroot}%{_datadir}/nextkde/shell/shared/qml
cp -rL shared/qml/. %{buildroot}%{_datadir}/nextkde/shell/shared/qml/
rm -rf %{buildroot}%{_datadir}/nextkde/shell/native
find %{buildroot}%{_datadir}/nextkde %{buildroot}%{_datadir}/shared \
    -type f \( -name CMakeLists.txt -o -name 'test_*' -o -name '*.test.mjs' -o -name '*.cpp' -o -name '*.h' -o -name '*.sh' \) -delete
mkdir -p %{buildroot}%{_datadir}/applications %{buildroot}%{_prefix}/lib/systemd/user
install -pm0644 packaging/desktop/kos-settings.desktop.in %{buildroot}%{_datadir}/applications/kos-settings.desktop
sed 's|@KOS_PLATFORM_EXEC@|%{_libexecdir}/kos-platform|' packaging/desktop/org.kos.Platform.desktop.in > %{buildroot}%{_datadir}/applications/org.kos.Platform.desktop
sed 's|@KOS_SHELL_EXEC@|%{_bindir}/quickshell|; s|-c kos|-p %{_datadir}/nextkde/shell|' packaging/desktop/org.kos.Shell.desktop.in > %{buildroot}%{_datadir}/applications/org.kos.Shell.desktop
sed 's|%%h/.local|%{_prefix}|g' packaging/systemd/kos-platform.service > %{buildroot}%{_prefix}/lib/systemd/user/kos-platform.service
sed 's|@CMAKE_INSTALL_FULL_LIBEXECDIR@|%{_libexecdir}|' services/data-service/systemd/kos-data.service.in > %{buildroot}%{_prefix}/lib/systemd/user/kos-data.service
sed 's|@QS_EXEC@|%{_bindir}/quickshell|; s|-c kos|-p %{_datadir}/nextkde/shell|; s|^Environment=QML2_IMPORT_PATH=.*|Environment=QML2_IMPORT_PATH=%{_datadir}/nextkde/shell:%{_libdir}/qt6/qml\nEnvironment=QML_IMPORT_PATH=%{_datadir}/nextkde/shell:%{_libdir}/qt6/qml|' packaging/systemd/kos-shell.service.in > %{buildroot}%{_prefix}/lib/systemd/user/kos-shell.service
mkdir -p %{buildroot}%{_datadir}/kos
printf '{"version":"%{version}","revision":"%{commit}","dirty":false,"tag":"v%{version}"}\n' > %{buildroot}%{_datadir}/kos/release.json

%check
# Packaging checks only. Native/unit/GUI runtime verification remains separate.
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
test -s %{buildroot}%{_libexecdir}/kos-platform
test -s %{buildroot}%{_libexecdir}/kos-data-service
test -s %{buildroot}%{_bindir}/kos-settings
test -s %{buildroot}%{_datadir}/nextkde/shell/shell.qml
test -s %{buildroot}%{_qt6_qmldir}/Kos/SurfaceShape/qmldir
# Glass configure silently skips its target if development dependencies fail.
find %{buildroot}%{_qt6_plugindir}/kwin/effects/plugins -name '*glass*.so' -print -quit | grep .
! grep -R '@QS_EXEC@\|@KOS_PLATFORM_EXEC@\|@KOS_SHELL_EXEC@' %{buildroot}%{_prefix}/lib/systemd/user %{buildroot}%{_datadir}/applications

%files
%license licenses/
%doc README.md
%{_bindir}/kos-settings
%{_libexecdir}/kos-platform
%{_libexecdir}/kos-data-service
%{_qt6_qmldir}/Kos/
%{_qt6_plugindir}/kwin/
%{_qt6_plugindir}/org.kde.kdecoration3/
%{_datadir}/kos/
%{_datadir}/nextkde/
%{_datadir}/shared/
%{_datadir}/applications/kos-settings.desktop
%{_datadir}/applications/org.kos.Platform.desktop
%{_datadir}/applications/org.kos.Shell.desktop
%{_prefix}/lib/systemd/user/kos-platform.service
%{_prefix}/lib/systemd/user/kos-data.service
%{_prefix}/lib/systemd/user/kos-shell.service
%{_datadir}/locale/*/LC_MESSAGES/kwin_effects_glass.mo

%changelog
* Sun Nov 01 2026 COPR packaging <nobody@fedoraproject.org> - 0.1.1-1
- Initial experimental pinned core package for Rawhide aarch64
