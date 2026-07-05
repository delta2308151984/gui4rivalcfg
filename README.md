# GUI4RivalCfg

<p align="center">
  <img src="images/logo.png" width="256" alt="GUI4RivalCfg Logo">
</p>

Grafische Oberfläche für rivalcfg unter Linux.

## Unterstützte Funktionen

- DPI-Konfiguration
- RGB-Konfiguration
- Reactive-Effekt
- Rainbow-Effekt
- RGB deaktivieren
- Dim Timer
- Sleep Timer
- Button-Mapping
- Batterieanzeige
- Deutsche und englische Benutzeroberfläche

## Screenshots

| DPI | RGB |
|-----|-----|
| ![](images/screenshots/dpi.png) | ![](images/screenshots/rgb.png) |

| Buttons | Info |
|----------|------|
| ![](images/screenshots/buttons.png) | ![](images/screenshots/info.png) |

## Voraussetzungen

- Linux
- Python 3
- Python-venv-Unterstützung

## Installation

1. `gui4rivalcfg-1.1.tar.gz` aus dem
   [v1.1-Release](https://github.com/delta2308151984/gui4rivalcfg/releases/tag/v1.1)
   herunterladen und entpacken.
2. Im entpackten Ordner ausführen:

```bash
./install.sh
```

Der Installer richtet Anwendung, Python-Umgebung, Starter und Menüeintrag
benutzerweit ein. Es sind keine Root-Rechte erforderlich. Anschließend kann
die Anwendung über das Anwendungsmenü oder im Terminal gestartet werden:

```bash
gui4rivalcfg
```

## Deinstallation

```bash
./uninstall.sh
```

## Start aus dem Quellcode

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```
