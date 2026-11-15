#!/usr/bin/env bash
# Host/source-worker packaging; never compiles a binary.
set -Eeuo pipefail
root=$(cd -- "$(dirname -- "$0")" && pwd)
package=${1:?Usage: build-srpm.sh PACKAGE NEW-OUTPUT-DIRECTORY}
out=${2:?Usage: build-srpm.sh PACKAGE NEW-OUTPUT-DIRECTORY}
[[ ! -e $out ]]
mkdir -p "$out"/{SPECS,SRPMS,BUILD,RPMS,BUILDROOT}
out=$(realpath "$out")
bash "$root/prepare-sources.sh" "$package" "$out/SOURCES"
mv "$out/SOURCES/$package.spec" "$out/SPECS/"
rpmbuild -bs --define "_topdir $out" --define '_buildhost localhost' --target aarch64 "$out/SPECS/$package.spec"
