# Changelog

All notable changes to this project are documented in this file.

## Unreleased

- Added LADCP profile support through the `[ladcp]` TOML section.
- Refactored profile KML generation for CTD, LADCP, and XBT.
- Added clearer validation for configuration keys, input files, and NetCDF
  variables.
- Updated `amazomix.toml` to use the bundled `OS_AMAZOMIX_ADCP.nc` file for
  LADCP data.
- Expanded the README with CLI usage, configuration details, and validation
  commands.
- Added regression tests for PIRATA-FR31, AMAZOMIX with LADCP, and XBT-only
  generation.
- Added GitHub Actions workflows for CI and tagged releases.
- Documented CI, release, and regression test commands.
- Removed the obsolete Travis CI configuration and badge.
- Set Python 3.11 as the default runtime and documented mamba-based environment
  creation and updates.
- Added README instructions for installing mamba before creating the project
  environment.
