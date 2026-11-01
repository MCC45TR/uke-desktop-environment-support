# UKE Desktop Environment Support

Desktop environment packaging for UKE Linux, with Fedora Rawhide AArch64 as
the current target. This repository is intended to be checked out as the
`uke-desktop-environment-support` submodule of
[uke-linux](https://github.com/MCC45TR/uke-linux/tree/Fedora).

| Directory | Status |
| --- | --- |
| [cutefish](cutefish/README.md) | Existing pinned Cutefish RPM packaging, migrated without payload changes. |
| [kde-next](kde-next/README.md) | NextKde packaging, maintained separately from the Cutefish migration. |

Run the packaging checks with RPM tools available on the host:

```sh
bash cutefish/tests/contract.sh
```

See each component's README for source preparation and validation limits.
This repository does not enable a desktop, build an image, or run upstream
source automatically. Runtime builds and device integration require separate
review and validation.

## Provenance and licensing

Cutefish packaging was extracted from `MCC45TR/uke-linux`, branch `Fedora`,
at commit `903038b3a9f540d6289bec5750d0863e817a6ec4`. Its original import is
[`aafc7bff593f3c887b4294b4bd9bfe90ec117ff9`](https://github.com/MCC45TR/uke-linux/commit/aafc7bff593f3c887b4294b4bd9bfe90ec117ff9).
The extracted history preserves that commit's author, date and message;
commit IDs change when repository paths are rewritten.

Original downstream files retain the source repository's [MIT license](LICENSE).
Upstream desktop source, branding, copyright and component licenses remain
with their respective owners. Cutefish source pins, archive checksums, RPM
license declarations and installed license notices are preserved unchanged.
