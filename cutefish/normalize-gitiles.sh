#!/usr/bin/env bash
# Gitiles uses request time in tar headers. Normalize metadata, preserving every
# source byte, mode and link. The resulting archive has its own pinned SHA-256.
set -Eeuo pipefail
input=${1:?input.tar.gz}
output=${2:?NEW-output.tar.gz}
[[ -f $input && ! -e $output ]]
parent=$(dirname -- "$output")
work=$(mktemp -d "$parent/.gitiles-normalize.XXXXXXXX")
trap 'rm -rf -- "$work"' EXIT
if tar -tzf "$input" | LC_ALL=C grep -E '(^/|(^|/)\.\.(/|$))'; then
    echo 'Unsafe archive path' >&2; exit 1
fi
mkdir "$work/tree"
chmod 755 "$work/tree"
tar -xzf "$input" --no-same-owner --same-permissions -C "$work/tree"
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner --format=gnu -cf - -C "$work/tree" . | gzip -n -9 > "$output"
