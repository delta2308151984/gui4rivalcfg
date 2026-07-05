#!/bin/sh
set -eu

DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"

rm -rf "$DATA_HOME/gui4rivalcfg"
rm -f "$DATA_HOME/applications/gui4rivalcfg.desktop"
rm -f "$HOME/.local/bin/gui4rivalcfg"

echo "GUI4RivalCfg wurde deinstalliert."
