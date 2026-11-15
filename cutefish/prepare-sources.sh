#!/usr/bin/env bash
# Source generation only. Binary builds run offline in COPR.
set -Eeuo pipefail
root=$(cd -- "$(dirname -- "$0")" && pwd)
package=${1:?Usage: prepare-sources.sh PACKAGE NEW-OUTPUT-DIRECTORY}
out=${2:?Usage: prepare-sources.sh PACKAGE NEW-OUTPUT-DIRECTORY}
[[ $package =~ ^[a-z0-9-]+$ && -f $root/packaging/$package.spec && ! -e $out ]]
mkdir -p "$out"
out=$(realpath "$out")
cp "$root/packaging/$package.spec" "$out/"
while read -r tag value _rest; do
    [[ $tag =~ ^(Source[0-9]*|Patch[0-9]*):$ ]] || continue
    case $value in
        https://*\#/*)
            archive=${value##*#/}
            url=${value%#/*}
            [[ $archive =~ ^[A-Za-z0-9._@-]+$ ]]
            record=$(awk -F '\t' -v file="$archive" '$2==file {print; n++} END {if(n!=1)exit 1}' "$root/sources.tsv")
            IFS=$'\t' read -r checksum _name locked_url normalization <<< "$record"
            [[ $url == "$locked_url" && $checksum =~ ^[0-9a-f]{64}$ ]]
            if [[ -f $root/referances/$archive ]]; then
                cp --reflink=auto "$root/referances/$archive" "$out/$archive"
            else
                curl --proto '=https' --tlsv1.2 -fL --retry 3 --max-time 600 "$url" -o "$out/$archive.part"
                if [[ ${normalization:-none} == gitiles-gnu-tar-mtime0-gzip9 ]]; then
                    bash "$root/normalize-gitiles.sh" "$out/$archive.part" "$out/$archive"
                    rm "$out/$archive.part"
                else mv "$out/$archive.part" "$out/$archive"; fi
            fi
            printf '%s  %s\n' "$checksum" "$out/$archive" | sha256sum --check --strict
            ;;
        *://*) echo 'Unpinned source URL' >&2; exit 1;;
        *)
            [[ $value =~ ^[A-Za-z0-9._@-]+$ ]]
            if [[ -f $root/packaging/$value ]]; then cp "$root/packaging/$value" "$out/"
            elif [[ -f $root/firstboot/$value ]]; then cp "$root/firstboot/$value" "$out/"
            elif [[ -f $root/session/$value ]]; then cp "$root/session/$value" "$out/"
            else cp "$root/$value" "$out/"; fi
            ;;
    esac
done < "$root/packaging/$package.spec"
