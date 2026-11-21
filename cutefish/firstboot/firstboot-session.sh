#!/usr/bin/bash
set -Eeuo pipefail
if [[ $(id -u) == 0 || -z ${XDG_RUNTIME_DIR:-} || ! -d $XDG_RUNTIME_DIR ]]; then
    echo 'Cutefish first-account setup: the unprivileged PAM session has no usable Wayland runtime directory.' >&2
    exit 1
fi
exec dbus-run-session /usr/libexec/uke-cutefish-firstboot-display
