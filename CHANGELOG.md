# Changelog

All notable changes to GUI4RivalCfg are documented in this file.

## [1.4.1] - 2026-09-13

### Fixed

- RGB disable now uses the color-zone options supported by the connected
  mouse instead of hard-coded Aerox options.
- Rival 3 shutdown now includes all three strip zones and the logo zone.
- Active reactive, rainbow, and lighting effects are stopped where supported,
  preventing them from turning the LEDs back on immediately.

## [1.4.0] - 2026-09-13

### Added

- Added a bilingual automatic updater to the information tab.
- New releases can be downloaded, SHA-256 verified, installed, and restarted
  directly from the application.
- The update button is only shown when a newer release with a verifiable
  archive is available.
- Download progress and success or failure messages are shown in the GUI and
  application log.

### Changed

- User settings are now stored below the XDG configuration directory
  (`~/.config/gui4rivalcfg` by default) and migrated from the legacy
  application-folder location so updates preserve them.

## [1.3.1] - 2026-09-13

### Changed

- The startup log now reports whether GUI4RivalCfg is up to date, a newer
  version is available, or the update check could not be completed.

## [1.3.0] - 2026-09-13

### Added

- The information tab now displays the installed GUI4RivalCfg version.
- On application startup, the latest GitHub release is checked asynchronously
  without blocking the user interface.
- The information tab displays the latest available version and a highlighted
  download link when an update is available.
- Failed or unavailable network checks are reported without preventing the
  application from starting.

## [1.2.3] - 2026-09-13

### Fixed

- The installer now checks whether the `rivalcfg` udev rules are installed
  and current.
- Missing USB access rules are installed automatically with a one-time
  administrator confirmation using `sudo` or `pkexec`.
- The installer tells the user to reconnect an already attached mouse so the
  new permissions take effect.

## [1.2.2] - 2026-09-13

### Fixed

- Detect DPI capabilities directly from the connected mouse's `rivalcfg`
  device profile, preventing the DPI tab from disappearing with differently
  formatted `rivalcfg --help` output.
- Correctly detect all Rival 3 RGB zones: strip top, strip middle, strip
  bottom, and logo.
- Use the Rival 3-specific RGB command-line options when writing colors.
- Load the last values persisted by `rivalcfg` for the connected device
  instead of displaying unrelated white defaults.
- Locate `rivalcfg` inside the application's virtual environment when it is
  not available through `PATH`.
- Display the actual GUI4RivalCfg and `rivalcfg` versions separately in the
  information tab.

### Compatibility

- DPI detection verified against the `rivalcfg` profiles for Rival 3,
  Rival 3 Gen 2, and Rival 3 Wireless.

## [1.2.1] - 2026-08-31

### Changed

- Made the installation instructions version-independent and linked them to
  the latest GitHub release.

## [1.2] - 2026-08-31

### Fixed

- Locate the bundled `rivalcfg` executable reliably from the application
  virtual environment.
