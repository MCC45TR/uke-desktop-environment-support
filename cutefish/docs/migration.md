# Rawhide split-package migration

15 November 2026. The qualified image path installs a fresh Rawhide root from
signed RPMs. It does not import an existing desktop root or execute a user
upgrade on a tablet.

`cutefish-desktop` now selects the independently packaged toolkit, framework,
core, compositor, display manager, icons, Qt integration, portal and applications.
The higher November 15 version replaces the former monolithic RPM. Split
components conflict with the older monolithic desktop, so a solver must replace
it in the same transaction rather than install overlapping providers alongside
it. `cutefish-desktop-devel` remains a compatibility selection for toolkit and
framework development packages. Image roots do not install development packages.

The optional `cutefish-suite` no longer selects the computer-use agent or Debian
installer. An agent already installed by an older suite is not automatically
removed; its existing consent and configuration are preserved. The separate
legacy agent source producer remains available. Plymouth data is optional and
is not activated by package installation. Uke session defaults use
`%config(noreplace)` for persistent preferences.

The signed split set passed metadata, individual SHA-256, sole-key signature
and regular-file ownership checks. The first session-config RPM was rejected
for duplicating upstream portal routing; release 2 removes that duplicate.
Rawhide fresh-root DNF installation, `dnf5 check` and installed desktop isolation
passed in the image workflow. These checks do not qualify an upgrade from an
existing November 1 installation. That transition needs its own real DNF
transaction and persistent-preference/rollback validation before it is promoted.
Fedora 44/45 have no new split-desktop image or upgrade acceptance. New source
producers exclude those targets; historical outputs remain recorded separately.

The dedicated Cutefish image adds secure first-account and greeter policy.
Installing desktop RPMs alone does not enable a display manager, create a human
account, change the selected session or establish graphical/hardware acceptance.
