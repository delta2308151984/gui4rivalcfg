# Changelog

All notable changes to GUI4RivalCfg are documented in this file.

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
