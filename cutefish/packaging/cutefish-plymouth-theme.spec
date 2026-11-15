Name:           cutefish-plymouth-theme
Version:        1.0^20261115
Release:        1%{?dist}
Summary:        Optional upstream Cutefish boot splash data
License:        GPL-3.0-only AND GPL-2.0-or-later
URL:            https://github.com/cutefishos/plymouth-theme
Source0:        https://codeload.github.com/cutefishos/plymouth-theme/tar.gz/d7f6543ae2bf5f7b83678472e053a85ee4063516#/plymouth-theme-d7f6543ae2bf5f7b83678472e053a85ee4063516.tar.gz
Source1:        GPL-3.0
BuildArch:      noarch
Requires:       plymouth plymouth-plugin-script

%description
Optional upstream splash data. Installation does not select a theme or change
the Uke boot image. This package supports the existing suite's upgrade path.

%prep
printf '%s  %s\n' 'ed1e2d8ac9dc0f09d5cd6ecd68ea0397e727c743065a2dad1e34f59c4862bb38' '%{SOURCE0}' | sha256sum -c -
%setup -q -n plymouth-theme-d7f6543ae2bf5f7b83678472e053a85ee4063516
cp %{SOURCE1} COPYING
%build
%install
mkdir -p %{buildroot}%{_datadir}/plymouth/themes
cp -a cutefish-logo cutefish-text %{buildroot}%{_datadir}/plymouth/themes/
rm -f %{buildroot}%{_datadir}/plymouth/themes/cutefish-text/*.in
%files
%license COPYING
%doc README.md
%{_datadir}/plymouth/themes/cutefish-logo/
%{_datadir}/plymouth/themes/cutefish-text/
%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 1.0^20261115-1
- Separate the optional data package without selecting a boot theme.
