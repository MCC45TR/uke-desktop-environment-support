#!/usr/bin/bash
set -Eeuo pipefail
export WAYLAND_DISPLAY=uke-firstboot
/usr/bin/cutefish-compositor --socket "$WAYLAND_DISPLAY" --no-xwayland &
compositor=$!
trap 'kill "$compositor" 2>/dev/null || :; wait "$compositor" 2>/dev/null || :' EXIT
for ((attempt=0;attempt<100;attempt++)); do
    kill -0 "$compositor"
    [[ ! -S $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY ]] || break
    sleep 0.1
done
[[ -S $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY ]]
/usr/libexec/uke-cutefish-firstboot
