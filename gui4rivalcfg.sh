#!/bin/sh
set -eu

APP_DIR="@APP_DIR@"
cd "$APP_DIR"

exec "$APP_DIR/.venv/bin/python" main.py
