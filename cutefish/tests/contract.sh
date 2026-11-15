#!/usr/bin/env bash
# Source/schema checks only; no binary is compiled on the development PC.
set -Eeuo pipefail
root=$(cd -- "$(dirname -- "$0")/.." && pwd)
jq -e '.schema==1 and .packaging_revision=="ea2f0a3f387b9f2094dbc50c92bd7595037b69c5" and
  .reference_iso.package_list_verified==true and .reference_iso.iso_payload_downloaded==false and
  (.sources|all(.[];(.revision|test("^[0-9a-f]{40}$")) and (.sha256|test("^[0-9a-f]{64}$"))))' "$root/sources.lock.json" >/dev/null
! jq -r '.sources[].project' "$root/sources.lock.json" | grep -Ex 'wallpapers|cutefish-installer|cutefish-computer-use|cutefish-webkit' || exit 1
for spec in "$root/packaging/"*.spec; do
    rpmspec --target aarch64 -P "$spec" >/dev/null
    # Network fetches belong to source generation, never prep/build/install/check.
    ! awk '/^%prep/{code=1} /^%files/{code=0} code{print}' "$spec" | grep -E 'curl |git clone|fetch-skia[.]sh|fetch-pdfium[.]sh' || exit 1
    ! grep -E 'systemctl (enable|disable)|--nogpgcheck' "$spec" || exit 1
done
while IFS=$'\t' read -r checksum archive url normalization; do
    [[ $checksum =~ ^[0-9a-f]{64}$ && $archive =~ ^[A-Za-z0-9._-]+$ && $url == https://* ]]
    jq -e --arg name "$archive" --arg sha "$checksum" --arg url "$url" '.sources|any(.[];.archive==$name and .sha256==$sha and .url==$url)' "$root/sources.lock.json" >/dev/null
done < "$root/sources.tsv"
for package in cutefish-toolkit cutefish-framework cutefish-core cutefish-compositor cutefish-dm cutefish-filemanager cutefish-icon-theme cutefish-settings cutefish-terminal cutefish-qt-plugins cutefish-system-monitor cutefish-text-editor cutefish-video-player cutefish-calendar cutefish-calculator cutefish-preview xdg-desktop-portal-cutefish; do
    test -f "$root/packaging/$package.spec"
    grep -Eq "^Requires: +$package >= 1[.]0\\^20261115$" "$root/packaging/cutefish-desktop.spec"
done
! grep -Ei '^Requires:.*(plasma-|kf[56]-|gdm|gnome-shell|cutefish-computer-use)' "$root/packaging/"*.spec || exit 1
! grep -E 'common-auth|common-account' "$root/packaging/cutefish-dm" "$root/packaging/cutefish-dm-greeter" || exit 1
bash -n "$root/prepare-sources.sh" "$root/build-srpm.sh" "$root/firstboot/firstboot-session.sh" "$root/firstboot/firstboot-display.sh"
printf '%s\n' 'PASS: split source locks, offline recipes, full runtime selection, credentials-free setup and activation boundaries'
