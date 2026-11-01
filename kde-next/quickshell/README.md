# Quickshell 0.3.2 candidate for mcc45tr/kdenext

Upstream latest release checked 2026-11-01: `v0.3.2`, published 2026-10-08.
Tag peeled to `4f508be500dea6e5732cc3d50382a0048b17e7b1`.
Canonical project: https://quickshell.org/ ; documented official GitHub mirror:
https://github.com/quickshell-mirror/quickshell .

## Status

Source inspected, candidate spec written. No CMake configure, compilation,
upstream tests, RPM build, install, or runtime launch has been executed here.
No repository enabled and no desktop activation performed.
A native Fedora build environment is required. The build requires
explicitly authorized isolated COPR execution followed by log review.
Source pinning does not mean byte-for-byte reproducible binaries on a moving
Rawhide dependency set; retain the resulting buildroot NEVRAs for provenance.

## Deliberate packaging choices

- Native aarch64 only; no prebuilt x86 payload or architecture substitution.
- Quickshell name/version provides the normal `quickshell >= 0.3` dependency.
- Qt/QML/Wayland private development headers are required. Upstream explicitly
  requires rebuilding Quickshell for **each Qt release** to avoid ABI crashes.
- Crash handler OFF to avoid cpptrace FetchContent and unverified distro
  cpptrace signal-safe unwinding support. All other upstream feature defaults
  remain enabled (Wayland, X11, tray, PipeWire, PAM, Polkit, UPower, networking,
  Bluetooth, notifications, etc.). No automatic shell activation.
- Main code LGPL-3.0-or-later; bundled Hyprland protocol declarations BSD-3-Clause;
  bundled wlroots protocols HPND-sell-variant. Both root license files and all
  embedded protocol copyright/permission notices are retained in binary RPM.
  Fedora's existing 0.2.1 spec independently lists the same three license IDs.
- No upstream patch proposed; local downstream packaging only. Upstream
  CONTRIBUTING requires human-authored contribution summaries and submission.

## Build, after approval and source checksum verification

Run in a Fedora packaging environment, not the user's tablet:

```sh
cd ..  # from kde-next/quickshell to kde-next
python3 fetch-sources.py
./pack-srpm.sh
copr-cli build --chroot fedora-rawhide-aarch64 mcc45tr/kdenext quickshell/SRPMS/*.src.rpm
```

The checks in the spec validate installed artifact presence and desktop-file
syntax only. A successful COPR build is not runtime acceptance. NextKDE's live
Wayland/KWin integration and target tablet graphics/input remain untested.

## Evidence

- Release: https://github.com/quickshell-mirror/quickshell/releases/tag/v0.3.2
- Build policy/deps: https://github.com/quickshell-mirror/quickshell/blob/4f508be500dea6e5732cc3d50382a0048b17e7b1/BUILD.md
- CMake: https://github.com/quickshell-mirror/quickshell/blob/4f508be500dea6e5732cc3d50382a0048b17e7b1/CMakeLists.txt
- Fedora baseline: https://src.fedoraproject.org/rpms/quickshell/raw/rawhide/f/quickshell.spec
