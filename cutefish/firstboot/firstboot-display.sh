#!/usr/bin/bash
set -Eeuo pipefail
export WAYLAND_DISPLAY=uke-firstboot
coproc compositor_ready {
    exec /usr/bin/cutefish-compositor --socket "$WAYLAND_DISPLAY" --no-xwayland \
        --ready-fd 3 3>&1 1>&2
}
compositor=$!
trap 'kill "$compositor" 2>/dev/null || :; wait "$compositor" 2>/dev/null || :' EXIT
ready_fd=${compositor_ready[0]:-}
if [[ -z $ready_fd ]] || ! IFS= read -r -N 1 -t 30 -u "$ready_fd" ready || [[ $ready != R ]]; then
    echo 'Cutefish first-account setup: compositor exited or did not initialize its display within 30 seconds.' >&2
    exit 1
fi
/usr/libexec/uke-cutefish-firstboot
