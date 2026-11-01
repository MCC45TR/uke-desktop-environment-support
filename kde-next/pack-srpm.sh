#!/bin/sh
# Source packing only. Never change -bs to -ba/-bb/-bp here.
set -eu
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$base"
python3 static-qa.py --sources
command -v rpmbuild >/dev/null
for pkg in nextkde quickshell; do
  if [ "$pkg" = nextkde ]; then top=$base; else top="$base/quickshell"; fi
  mkdir -p "$top/BUILD" "$top/BUILDROOT" "$top/RPMS" "$top/SRPMS"
  rpmbuild --define "_topdir $top" --define '_qt6_qmldir /usr/lib64/qt6/qml' \
    --define '_qt6_plugindir /usr/lib64/qt6/plugins' --define 'dist .fc46' \
    --target aarch64 -bs "$top/SPECS/$pkg.spec"
done
