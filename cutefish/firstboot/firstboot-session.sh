#!/usr/bin/bash
set -Eeuo pipefail
[[ $(id -u) != 0 && -n ${XDG_RUNTIME_DIR:-} && -d $XDG_RUNTIME_DIR ]]
exec dbus-run-session /usr/libexec/uke-cutefish-firstboot-display
