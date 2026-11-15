Name:           wvkbd
Version:        0.21^20261115
Release:        1%{?dist}
Summary:        Wayland touch keyboard with input-method-v2 automatic visibility
License:        GPL-3.0-only
URL:            https://github.com/jjsullivan5196/wvkbd
ExclusiveArch:  aarch64
Source0:        https://codeload.github.com/jjsullivan5196/wvkbd/tar.gz/4ae78249f39e1c9ce67a939d338aab2ad1e3d919#/wvkbd-4ae78249f39e1c9ce67a939d338aab2ad1e3d919.tar.gz
BuildRequires:  gcc make scdoc pkgconfig(wayland-client) pkgconfig(xkbcommon) pkgconfig(pangocairo)

%description
The upstream wvkbd mobile international keyboard. It uses Wayland virtual
keyboard, layer shell and input-method-v2 protocols. Fedora Rawhide did not
provide this package at the image source-lock date. No desktop is enabled.

%prep
printf '%s  %s\n' '73d641c8f0aa82a5d36fad97c6106a21da96396d25d09c280b76b74803c273b6' '%{SOURCE0}' | sha256sum -c -
%setup -q -n wvkbd-4ae78249f39e1c9ce67a939d338aab2ad1e3d919
# Preserve Fedora hardening flags alongside upstream's feature definitions.
sed -i 's/^CFLAGS = /CFLAGS += /' config.mk

%build
%set_build_flags
%make_build CC="$CC"

%install
%make_install PREFIX=%{_prefix} MANPREFIX=%{_mandir}

%check
test -x %{buildroot}%{_bindir}/wvkbd-mobintl

%files
%license LICENSE
%doc README.md
%{_bindir}/wvkbd-mobintl
%{_mandir}/man1/wvkbd.1*

%changelog
* Sun Nov 15 2026 MCC45TR <75160848+MCC45TR@users.noreply.github.com> - 0.21^20261115-1
- Package the pinned upstream keyboard for the Cutefish input-method relay.
