# mcc45tr/kdenext — source packaging checkpoint

Target: **fedora-rawhide-aarch64 only**. Experimental package, not hardware certification.
Latest stable NextKDE release checked 2026-11-01: **v0.1.1**, published 2026-10-20,
pinned commit **2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5**.
Quickshell **0.3.2**, commit **4f508be500dea6e5732cc3d50382a0048b17e7b1**.

## What this contains

NextKDE is a Quickshell desktop shell layered on KDE Plasma Wayland, not a KDE
fork or merely a theme. Core package includes QML shell, native SurfaceShape
module, C++ platform daemon, Go data daemon, Settings application, KWin Bridge,
Dock, Stage Animation, Context Menu Input, Glass effects and window decoration.

Deliberately excluded: spatial/ONNX depth processing and downloaded models,
Calendar/Calculator/Todo/Weather optional apps, legacy Music, ListenFree/private
SDK, SDDM/lock-screen takeover. The core weather data daemon remains included.
No prebuilt x86 executable is packaged. Committed QSB shader assets are portable
Qt shader containers, not x86 code; sources remain included. Shader runtime
compatibility still needs actual rendering tests.

The package never runs kosctl, installers, sudo, remote downloads, user session
activation or autostart scriptlets. It uses /usr/share/nextkde/shell with the
Quickshell -p option; it does not overwrite ~/.config/quickshell/kos. Settings
fallback paths are adapted to the installed location. All user state remains
under Quickshell's upstream pinned StateDir. Existing manually installed
NextKDE units can shadow packaged units and must be reviewed before activation.

## Sources and reproducibility

Run `python3 fetch-sources.py` from this directory. It fetches the exact
NextKDE Git commit into a temporary bare repository, generates `git archive`
with `gzip -n`, downloads pinned Go/Quickshell source archives and checks
`SOURCE-SHA256SUMS`. No upstream code or installation scripts are executed.
Archive/compression tool changes may cause checksum failure: review differences,
do not silently accept or regenerate a mismatched checksum.

Go dependencies were downloaded as source ZIPs from the canonical Go proxy:
- https://proxy.golang.org/github.com/fsnotify/fsnotify/@v/v1.10.1.zip
- https://proxy.golang.org/golang.org/x/sys/@v/v0.13.0.zip

`python3 prepare-vendor.py` does only archive/hash processing (no upstream code
execution). It implements Go dirhash h1 and checks the pinned upstream go.sum:
- fsnotify: `h1:b0/UzAf9yR5rhf3RPm9gf3ehBPpf0oZKIjtpKrx59Ho=`
- x/sys: `h1:Af8nKPmuFypiUBjVoU9V20FiaFXOcuZI21p0ycVYYGE=`

Vendor tar has sorted paths, fixed modes/timestamps, no network build dependency.
Actual Go build sets GOPROXY=off, GOSUMDB=off, GOTOOLCHAIN=local, -mod=vendor.
No source build has yet run. Go >=1.26 is required by this exact release.
Source pinning does not promise byte-identical binaries against changing
Rawhide; preserve COPR buildroot NEVRAs/build logs and rebuild for Qt/KWin ABI changes.

## License inventory

Candidate binary-package expression: GPL-3.0-only AND GPL-2.0-or-later AND MIT
AND BSD-3-Clause AND Apache-2.0. Root GPLv3, marked GPL2-or-later KWin portions,
MIT SurfaceShape protocol/Flow, BSD-3-Clause Bruneton wallpaper and Go modules,
Apache-2.0-derived Cam16/HCT color utilities. Original notices plus full license
texts and x/sys patent grant are copied under uniquely named license files.
Quickshell's separate spec retains LGPLv3/GPLv3 and all eight bundled Wayland
protocol notices; see its README and protocol audit. This is a source-based
packaging inventory, not a formal distribution legal review.

## Build order and gates

1. Run `python3 static-qa.py --sources` and verify SRPM metadata. Review specs and their literal scripts.
2. Obtain explicit authorization for isolated COPR execution of the two pinned
   upstream projects. Source RPM creation with `rpmbuild -bs` only packs sources;
   it does not execute upstream %prep/%build/%install/%check.
3. Submit Quickshell SRPM to mcc45tr/kdenext with ONLY fedora-rawhide-aarch64.
   Wait for terminal success and repository publication. Do not enable another
   third-party COPR. Crash-handler OFF prevents cpptrace FetchContent downloads.
4. Submit NextKDE SRPM in the same chroot; inspect all native build logs and RPM
   file manifests. First-build failures are expected to require dependency/path
   adjustment, not silent exclusion of core components. RPM Requires demands
   quickshell >=0.3 and <0.4 because official Rawhide currently remains 0.2.1git.
5. Confirm aarch64 RPM architecture, dependencies resolve, native plugin outputs
   include all five effects + decoration + SurfaceShape; verify no /home or
   buildroot references and no scriptlets that activate desktop services.
6. Run upstream relevant native/data/logic tests in a dedicated Fedora VM/CI;
   package %check currently validates only desktop syntax and core output presence.
7. A real Plasma Wayland VM/target session is a separate authorized acceptance
   stage: compositor/plugin load, Settings IPC, dock, screenshots, notifications,
   graphics/input, fresh install, upgrade, removal and rollback. Fedora SELinux
   labels must be checked. No tablet modification or installation is authorized.

## State and limitations

Static source and dependency archive checks are performed locally; CMake,
compiler, upstream tests and desktop execution have NOT run. Candidate specs
are intended for the first isolated test build, not a claim of working RPMs.
Do not tell the user to enable/install the repository until actual builds succeed.
KWin/Qt private APIs require rebuilds as Rawhide advances. Stable v0.1.1 may need
compatibility patches for current Rawhide; never replace it with unpinned main
or claim the pinned release inherits newer main fixes.

## Primary evidence

- https://github.com/NextKde/NextKde/releases/tag/v0.1.1
- https://github.com/NextKde/NextKde/tree/2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5
- https://github.com/NextKde/NextKde/blob/2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5/docs/GettingStarted.md
- https://packages.fedoraproject.org/pkgs/quickshell/quickshell/fedora-rawhide.html
- https://github.com/quickshell-mirror/quickshell/releases/tag/v0.3.2

## Historical local source-package result (2026-11-01)

The following records the original scratch-workspace experiment. Its binary
tooling, source archives and SRPM outputs are deliberately not committed.
The portable `pack-srpm.sh` now uses the host Fedora RPM packaging tools.
This historical result does not validate newly packed or published RPMs.

Trusted Debian RPM 4.20.1+dfsg-3 tooling and required libraries were downloaded
from deb.debian.org, checked against SHA256 values in Debian trixie's package
index and extracted under `rpm-tools/root/`. Nothing was installed into the
host. `pack-srpm.sh` only invokes `rpmbuild -bs --target aarch64`; both specs
were checked to contain no source-controlled parse-time shell/Lua macros.

Produced unsigned source packages:
- `quickshell/SRPMS/quickshell-0.3.2-1.fc46.kdenext.src.rpm`
- `SRPMS/nextkde-0.1.1-1.fc46.src.rpm`

`rpmkeys --checksig` reports **digests OK** for both (not a signing claim).
`check-srpm.py` independently decompresses/reads the CPIO payload and proves
all 2 Quickshell / 6 NextKDE payload files match the local source/spec bytes.
The original scratch-workspace `static-qa.py` proved the NextKDE source archive matches all 1742 tracked
entries of the pinned release, checks 644 vendor archive entries for safe
paths/fixed metadata, and confirms aarch64-only specs/no activation scriptlets.
These checks do NOT execute %prep, CMake, compiler, upstream tests or runtime.

The source packages are ready for an authorized **first test build**. They
are not proof that dependency resolution or native compilation will succeed.
RPM source-package headers report aarch64 because they were packed with that
target; this does not claim any compiled aarch64 binary exists yet.
