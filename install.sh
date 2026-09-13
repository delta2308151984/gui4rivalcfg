#!/bin/sh
set -eu

APP_NAME="gui4rivalcfg"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
APP_DIR="$DATA_HOME/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$DATA_HOME/applications"
SOURCE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

command -v python3 >/dev/null 2>&1 || {
    echo "Fehler: Python 3 ist nicht installiert." >&2
    exit 1
}

mkdir -p "$APP_DIR" "$APP_DIR/images" "$BIN_DIR" "$DESKTOP_DIR"

cp "$SOURCE_DIR"/*.py "$APP_DIR/"
cp "$SOURCE_DIR/requirements.txt" "$APP_DIR/"
cp "$SOURCE_DIR/CHANGELOG.md" "$APP_DIR/"
cp -R "$SOURCE_DIR/images/." "$APP_DIR/images/"

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

RIVALCFG_BIN="$APP_DIR/.venv/bin/rivalcfg"
UDEV_STATUS=$("$RIVALCFG_BIN" --print-debug 2>/dev/null || true)

if printf '%s\n' "$UDEV_STATUS" | grep -Fq "udev rules installed: True" \
    && printf '%s\n' "$UDEV_STATUS" | grep -Fq "udev rules up to date: True"; then
    echo "Die rivalcfg-udev-Regeln sind bereits aktuell."
else
    echo "Die USB-Zugriffsregeln für SteelSeries-Geräte werden eingerichtet."
    echo "Dafür ist einmalig eine Administratorbestätigung erforderlich."

    if [ "$(id -u)" -eq 0 ]; then
        "$RIVALCFG_BIN" --update-udev
    elif command -v sudo >/dev/null 2>&1 && [ -t 0 ]; then
        sudo "$RIVALCFG_BIN" --update-udev
    elif command -v pkexec >/dev/null 2>&1; then
        pkexec "$RIVALCFG_BIN" --update-udev
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$RIVALCFG_BIN" --update-udev
    else
        echo "Fehler: Weder sudo noch pkexec ist verfügbar." >&2
        echo "Installiere die udev-Regeln anschließend als root mit:" >&2
        echo "  $RIVALCFG_BIN --update-udev" >&2
        exit 1
    fi
fi

sed "s|@APP_DIR@|$APP_DIR|g" \
    "$SOURCE_DIR/gui4rivalcfg.sh" > "$BIN_DIR/gui4rivalcfg"
chmod +x "$BIN_DIR/gui4rivalcfg"

sed \
    -e "s|@EXEC@|$BIN_DIR/gui4rivalcfg|g" \
    -e "s|@ICON@|$APP_DIR/images/logo_clean.png|g" \
    "$SOURCE_DIR/gui4rivalcfg.desktop" \
    > "$DESKTOP_DIR/gui4rivalcfg.desktop"

chmod +x "$DESKTOP_DIR/gui4rivalcfg.desktop"

echo "GUI4RivalCfg wurde installiert."
echo "Start: $BIN_DIR/gui4rivalcfg"
echo "Falls die Maus bereits angeschlossen war, ziehe sie einmal ab und wieder an."
