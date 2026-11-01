# Candidate package: build/installation/runtime validation remains required.
%global commit 4f508be500dea6e5732cc3d50382a0048b17e7b1
%global __cmake_in_source_build 0

Name:           quickshell
Version:        0.3.2
Release:        1%{?dist}.kdenext
Summary:        QtQuick desktop shell toolkit for NextKDE
License:        LGPL-3.0-or-later AND BSD-3-Clause AND HPND-sell-variant
URL:            https://quickshell.org/
Source0:        https://github.com/quickshell-mirror/quickshell/archive/%{commit}/quickshell-%{commit}.tar.gz
ExclusiveArch:  aarch64

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  python3
BuildRequires:  qt6-rpm-macros
BuildRequires:  cmake(Qt6Core) >= 6.6
BuildRequires:  cmake(Qt6CorePrivate)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6QuickPrivate)
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  cmake(Qt6WaylandClientPrivate)
BuildRequires:  cmake(CLI11)
BuildRequires:  cmake(VulkanHeaders)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(xcb)
BuildRequires:  spirv-tools
Requires:       qt6-qtsvg%{?_isa}
Requires:       (qt6-qtwayland%{?_isa} if qt6-qtbase%{?_isa} < 6.10)
Provides:       desktop-notification-daemon = %{version}-%{release}
Provides:       PolicyKit-authentication-agent = %{version}-%{release}

%description
Quickshell is a QtQuick toolkit for desktop bars, widgets and shells.
This pinned aarch64 package supplies NextKDE's required 0.3.x runtime.
The crash-handler feature is disabled; all other upstream default features
are retained. It neither starts a shell nor changes desktop settings.

%prep
%autosetup -n %{name}-%{commit}
# Keep copyright and permission text of every bundled Wayland protocol in
# the binary RPM, not just the LGPL license covering the main project.
python3 - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET
out = []
for path in sorted(Path('src/wayland').rglob('*.xml')):
    root = ET.parse(path).getroot()
    for entry in root.findall('copyright'):
        out.append(str(path) + '\n' + ''.join(entry.itertext()).strip() + '\n')
Path('PROTOCOL-LICENSES.txt').write_text('\n'.join(out))
assert out, 'Protocol copyright notices missing'
PY

%build
# Never FetchContent/download code in the build sandbox. Crash support would
# require cpptrace with signal-safe libunwind support; package it separately
# before re-enabling rather than silently downloading it at configure time.
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DDISTRIBUTOR="Fedora COPR (mcc45tr/kdenext)" \
    -DGIT_REVISION=%{commit} \
    -DINSTALL_QMLDIR=%{_qt6_qmldir} \
    -DCRASH_HANDLER=OFF \
    -DVENDOR_CPPTRACE=OFF \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.quickshell.desktop
test -x %{buildroot}%{_bindir}/quickshell
test -L %{buildroot}%{_bindir}/qs
test -d %{buildroot}%{_qt6_qmldir}/Quickshell

%files
%license LICENSE LICENSE-GPL PROTOCOL-LICENSES.txt
%doc README.md BUILD.md
%{_bindir}/qs
%{_bindir}/quickshell
%{_datadir}/applications/org.quickshell.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg
%{_qt6_qmldir}/Quickshell/

%changelog
* Sun Nov 01 2026 COPR Packaging <noreply@example.invalid> - 0.3.2-1.kdenext
- Pin upstream 0.3.2 for Fedora Rawhide aarch64 NextKDE experiments.
