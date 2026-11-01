# KDE Next / NextKDE packaging

Experimental, pinned **Fedora Rawhide / aarch64-only** RPM packaging for
NextKDE 0.1.1 and its Quickshell 0.3.2 dependency. This directory contains
maintainable packaging inputs, not a desktop source fork or working binaries.
Native compilation, dependency resolution, runtime and tablet acceptance remain
unverified. Nothing here enables services or changes the user's desktop.

## Review and prepare

```sh
cd kde-next
python3 static-qa.py                 # no downloads or upstream execution
python3 fetch-sources.py             # retrieve pinned sources, verify hashes
python3 static-qa.py --sources
./pack-srpm.sh                       # requires Fedora RPM tools; source packing only
python3 check-srpm.py                # inspect packed source payloads
```

Requirements: Python 3, Git, gzip; source packing additionally needs a trusted
Fedora RPM packaging environment with `rpmbuild`. Network retrieval requires
GitHub and proxy.golang.org access. `fetch-sources.py` generates the NextKDE
archive from its immutable commit, verifies downloaded SHA256 values and Go
module h1 hashes, then creates a deterministic vendor archive. Failures must
be investigated rather than bypassed. These commands never compile upstream
code, run upstream installation scripts, or submit COPR builds.

Source tarballs, module ZIPs, vendor archives, RPMs, downloaded toolchains and
credentials are intentionally excluded from Git. `SOURCE-SHA256SUMS` records
source inputs; `PACKAGING-SHA256SUMS` records the committed packaging text.
`BUILD-PLAN.md` records provenance, license inventory, limitations and the
separate authorization/acceptance gates for an isolated native COPR build.
Review upstream code and the RPM macros/toolchain before any real build.

## Layout

- `SPECS/nextkde.spec`: pinned NextKDE core shell package.
- `quickshell/SPECS/quickshell.spec`: pinned compatible Quickshell package.
- `SOURCES/*.txt`: upstream license texts and source-based license inventory.
- `quickshell/PROTOCOL-LICENSES-audit.txt`: retained protocol license evidence.

Upstream licensing remains attached to its respective source components; the
license inventory is not a legal certification. This package is not ready to
recommend installation until native build and runtime gates pass.
