Name:           cutefish-desktop
Version:        1.0^20261115
Release:        1%{?dist}
Summary:        Cutefish Wayland desktop and core application set
License:        BSD-3-Clause
URL:            https://github.com/cutefishos
Source0:        LICENSE
Source100:      sources.lock.json
BuildArch:      noarch
Requires:       cutefish-toolkit >= 1.0^20261115
Requires:       cutefish-framework >= 1.0^20261115
Requires:       cutefish-core >= 1.0^20261115
Requires:       cutefish-compositor >= 1.0^20261115
Requires:       cutefish-dm >= 1.0^20261115
Requires:       cutefish-icon-theme >= 1.0^20261115
Requires:       cutefish-filemanager >= 1.0^20261115
Requires:       cutefish-settings >= 1.0^20261115
Requires:       cutefish-terminal >= 1.0^20261115
Requires:       cutefish-system-monitor >= 1.0^20261115
Requires:       cutefish-text-editor >= 1.0^20261115
Requires:       cutefish-video-player >= 1.0^20261115
Requires:       cutefish-calendar >= 1.0^20261115
Requires:       cutefish-calculator >= 1.0^20261115
Requires:       cutefish-preview >= 1.0^20261115
Requires:       cutefish-qt-plugins >= 1.0^20261115
Requires:       xdg-desktop-portal-cutefish >= 1.0^20261115

%description
Install the upstream Cutefish desktop and core applications from separate RPMs.
The metapackage replaces the old monolithic payload in one RPM transaction.
No display manager is enabled. First-account setup is an image policy.
The Debian installer, Unsplash wallpapers and computer-control agent are not
part of this default desktop selection.

%package devel
Summary:        Compatibility selection for Cutefish development packages
Requires:       cutefish-toolkit-devel >= 1.0^20261115
Requires:       cutefish-framework-devel >= 1.0^20261115

%description devel
Preserves the old development package selection during the split migration.

%prep
cp %{SOURCE0} LICENSE
cp %{SOURCE100} sources.lock.json
%build
%install
install -Dm644 sources.lock.json %{buildroot}%{_docdir}/%{name}/sources.lock.json
%files
%license LICENSE
%doc %{_docdir}/%{name}/sources.lock.json
%files devel
%license LICENSE

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-1
- Replace the monolithic payload with the full independently built RPM set.
