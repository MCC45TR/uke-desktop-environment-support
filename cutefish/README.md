# Cutefish Fedora packaging

21 November 2026. Fedora Rawhide AArch64. The signed packages are built under
the `cutefish-desktop` COPR package in Uke Unstable. The source RPMs and
individual binary package names are retained. [Uke Unstable Cutefish builds](https://copr.fedorainfracloud.org/coprs/mcc45tr/uke-linux-unstable/package/cutefish-desktop/)

Existing Cutefish images can follow the repository switch in the
[Uke builder guide](https://github.com/MCC45TR/uke-fedora-builder/blob/main/docs/PUBLIC-BUILD.md).

Sources follow the published ARM64 nightly package list and commit manifest
for `cutefish-1.0-nightly-20261115-1345-arm64.iso`. The ISO checksum and package
list were retrieved; the 1.6 GB ISO payload was not downloaded or independently
inspected. `sources.lock.json` pins the packaging revision and every downloaded
source archive. Source generation verifies SHA-256 before handing sources to
COPR; binary builds have network access disabled.

Each upstream component has its own source RPM. Toolkit and framework headers
are separate development subpackages. Original Fedora libraries remain the
runtime providers. Skia GN requires the original upstream Python generators
on the build host only; no project Python runtime is installed. PDFium source
closure, native first-account setup and image composition remain in progress.

Upstream source and branding belong to [Cutefish](https://github.com/cutefishos).
The default image excludes Unsplash wallpapers, the Debian installer, the
optional computer-control server and WebKit.
Initial API requests used the Swagger `chroot_names` field, which the actual
form ignored, so those builds also ran for Fedora 44/45. Later requests use
`chroots`, with the sole Rawhide target verified from returned build state.
The new desktop metapackage is released only to Rawhide after qualification;
Fedora 44/45 are not image targets or qualified upgrade claims in this work.
Installing the display-manager RPM must not enable it or switch desktops.

To prepare one source RPM, without compiling any binary:

```bash
bash build-srpm.sh cutefish-toolkit ../build/toolkit
```

A fresh-root signed DNF installation, file ownership transition, first-account
setup, PAM/SELinux and physical GPU/touch tests are required before publishing
an installable release. Build receipts and image manifests record those stages
separately.
