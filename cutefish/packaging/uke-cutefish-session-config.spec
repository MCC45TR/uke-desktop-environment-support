Name:           uke-cutefish-session-config
Version:        1.0.0
Release:        1%{?dist}
Summary:        Cutefish image defaults and a freely licensed Uke background
License:        BSD-3-Clause
URL:            https://github.com/MCC45TR/uke-desktop-environment-support
Source0:        services.conf
Source1:        compositor.conf
Source2:        uke-wvkbd.desktop
Source3:        portals.conf
Source4:        default.svg
Source5:        LICENSE
BuildArch:      noarch
Requires:       cutefish-core >= 1.0^20261115
Requires:       cutefish-dm >= 1.0^20261115
Requires:       xdg-desktop-portal-cutefish >= 1.0^20261115
Requires:       wvkbd >= 0.21^20261115
Requires:       rsms-inter-fonts google-noto-sans-mono-vf-fonts
Requires:       uke-cutefish-wallpapers = %{version}-%{release}

%description
Defaults for new accounts in the Cutefish image. Existing preferences are not
replaced. The compositor demand-starts its selected input-method provider.

%package -n uke-cutefish-wallpapers
Summary:        Original freely licensed gradient background for Uke Cutefish
BuildArch:      noarch

%description -n uke-cutefish-wallpapers
Original vector background distributed under BSD-3-Clause. No Unsplash images.

%prep
cp %{SOURCE5} LICENSE
%build
%install
install -Dm644 %{SOURCE0} %{buildroot}%{_sysconfdir}/skel/.config/cutefish/services.conf
install -Dm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/skel/.config/cutefish/compositor.conf
install -Dm644 %{SOURCE1} %{buildroot}%{_localstatedir}/lib/cutefish-greeter/.config/cutefish/compositor.conf
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/applications/uke-wvkbd.desktop
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/xdg-desktop-portal/cutefish-portals.conf
install -Dm644 %{SOURCE4} %{buildroot}%{_datadir}/backgrounds/uke-cutefish/default.svg

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/skel/.config/cutefish/*.conf
%{_datadir}/applications/uke-wvkbd.desktop
%{_datadir}/xdg-desktop-portal/cutefish-portals.conf
%attr(0700,cutefish-greeter,cutefish-greeter) %dir %{_localstatedir}/lib/cutefish-greeter/.config
%attr(0700,cutefish-greeter,cutefish-greeter) %dir %{_localstatedir}/lib/cutefish-greeter/.config/cutefish
%attr(0600,cutefish-greeter,cutefish-greeter) %config(noreplace) %{_localstatedir}/lib/cutefish-greeter/.config/cutefish/compositor.conf

%files -n uke-cutefish-wallpapers
%license LICENSE
%{_datadir}/backgrounds/uke-cutefish/

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0.0-1
- Add new-account defaults, portal routing and a demand-started touch keyboard.
