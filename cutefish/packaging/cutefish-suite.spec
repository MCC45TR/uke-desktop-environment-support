Name:           cutefish-suite
Version:        1.1
Release:        1%{?dist}
Summary:        Cutefish desktop application suite and original Fedora fonts
License:        BSD-3-Clause
URL:            https://github.com/MCC45TR/uke-desktop-environment-support/tree/main/cutefish
Source0:        LICENSE
BuildArch:      noarch
Requires:       cutefish-desktop >= 1.0^20261115
Requires:       cutefish-plymouth-theme >= 1.0^20261115
Requires:       rsms-inter-fonts google-noto-color-emoji-fonts

%description
The complete separately packaged desktop, applications, optional splash data
and original Fedora fonts. Installation does not switch display managers or
select a boot theme. Computer-control software is an explicit optional package;
the Debian installer and Unsplash wallpapers are excluded.

%prep
cp %{SOURCE0} LICENSE
%build
%install
%files
%license LICENSE

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.1-1
- Select the split desktop without installing a computer-control agent.
