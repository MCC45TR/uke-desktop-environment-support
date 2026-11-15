# Rawhide split-package and image audit

15 November 2026. Native Rawhide AArch64 RPM qualification completed. No image or hardware
acceptance is established by this package record.

| Area | Existing state | New source policy |
| --- | --- | --- |
| COPR | `mcc45tr/cutefish`, Pulp, offline binary builds, three AArch64 targets | Preserve project and signing key; qualify the migration on Rawhide only |
| Published desktop | `1.0^20261101-5`, build 11240635; toolkit/framework/core bundled | Independent source RPMs; development files remain separate |
| Source version | November 1 fork pins | Published November 15 ARM64 nightly commits, packaging `ea2f0a3f387b9f2094dbc50c92bd7595037b69c5` |
| Nightly evidence | No current ISO match in old Uke packaging | Package list, commit manifest and checksum retrieved; full ISO not downloaded/inspected |
| Display manager | Uke image used GDM and a public test account | Upstream Cutefish DM; locked root; no human account in the image |
| First account | No Cutefish onboarding | Dedicated unprivileged Qt session and a one-request native root provisioner; runtime acceptance pending |
| Touch keyboard | No validated provider | In-process setup keyboard; pinned upstream wvkbd via compositor input-method-v2 for normal/greeter sessions |
| Turkish | Old builder expected GDM/GNOME catalogs | Preserve complete supplied catalogs and Turkish glibc/fonts; upstream provides no Turkish Cutefish UI catalogs |
| Wallpaper | Upstream Unsplash content excluded | Original BSD-licensed vector artwork |
| Agent/live installer | Included in old optional suite | Excluded from the new image and desktop metapackage |
| Kernel/hardware | Cumulative Uke unstable RPMs | Same signed cohort and existing image integrity chain; no kernel build or tablet write |

`build-order.tsv` records source-RPM build dependencies. Toolkit and framework
must be published before consumers are built. The desktop metapackage is
published only after the entire runtime set succeeds and is visible to DNF.
The old desktop-development selection is preserved as a small compatibility
metapackage. The optional Plymouth data RPM no longer requires an exact old
monolithic desktop, preserving the old suite's upgrade closure. The initial target-selection field was ignored by the frontend, so those jobs
also emitted Fedora 44/45 results. Subsequent requests use the actual `chroots`
form field and verify the sole Rawhide target. No new desktop metapackage is
published for Fedora 44/45; those targets have no new image acceptance.

Source locks include Skia m156, the exact PDFium 8158 directories used by the
framework, Chromium build headers, dragonbox, fast_float and their licenses.
All are declared source inputs and hash-checked before extraction. The source
worker alone downloads them. Skia's original Python build generators execute
only on the COPR host. No project Python is installed in the target.

First-account state is private and journaled. A request must come from the
`uke-setup` UID over a mode-0600 local socket. The helper validates every field,
serializes requests, refuses pre-existing human accounts, applies the Fedora
password-quality policy and passes the password over a private pipe to PAM's
`chpasswd`. Retry after interruption is restricted to the journaled account;
no user/home is deleted. The completion file is synchronized only after
account, password, locale, timezone and wheel setup succeed. The GUI has no
root shell, useradd permission or reusable administrative authorization.

Required remaining evidence: fresh-root
DNF installation and upgrade from the old desktop/suite; no KDE/GDM/GNOME
Shell in the installed closure; PAM, systemd and SELinux; first-account
interruption/refusal/success tests; normal/greeter touch keyboard; Cutefish
applications, GPU/DRM, scaling, clipboard and portals on the physical Uke.
Test artifacts must remain explicitly hardware-untested; publication is gated
on a separate physical acceptance record.

Gitiles archive responses varied in request-time tar metadata. Release 2 of the
framework normalizes GNU tar owner/group/time headers and gzip time while
preserving source bytes, modes and links. Two independently retrieved constants
archives produce identical normalized bytes. The normalized archive SHA-256 is
sealed in the spec and lock; the first observed download hash is retained as
provenance. Source workers perform exactly the same normalization before checks.

Fedora libical 4 changes recurrence ownership, arrays and several function
names. Calendar carries a narrowly scoped source adaptation, clones borrowed
rules before modification and releases references with RAII. The original
Fedora libical RPM remains the provider. The COPR build enables upstream core
recurrence tests; all 44 core recurrence tests passed in build 11331118.

Independent signed-RPM file comparison rejected the first Uke session-config
RPM: it duplicated the upstream portal routing path with different contents.
Session-config release 2 removes that duplicate and keeps upstream's own
portal routing. The failed ownership audit is retained; no image
was composed from the conflicting set.

The upstream portal configuration selects GTK for unimplemented interfaces,
Cutefish for Settings/FileChooser/Inhibit/ScreenCast and GNOME Keyring for
Secret. The desktop metapackage explicitly requires original Fedora's GTK
backend. Upstream advertises no Screenshot portal interface; the separate
native screenshot utility and ScreenCast still require physical validation.

The qualified set contains 28 non-debug signed AArch64/noarch RPMs from 24
source builds. Repository primary checksums, individual SHA-256 values and
signatures were verified with the sole pinned Cutefish signing key. Comparing
1,702 regular file paths found no conflicting payloads.
[qualified-rpms.tsv](qualified-rpms.tsv) records the exact package/build/hash
cohort. This includes development and optional data packages; the image profile
selects only its explicit runtime closure. The source-generated firstboot
validator passed in the native COPR build; GUI/PAM/systemd runtime acceptance
remains open.
