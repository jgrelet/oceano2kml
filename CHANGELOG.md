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
- Added `TODO.md` with future documentation and screenshot tasks.
- Added `Taskfile.yml` for task runner (replaces Makefile) with commands for
  testing, KML generation, and CI pipeline.
- Added `docs/configuration.md` with complete TOML configuration schema,
  including all global keys, instrument sections, and examples.
- Added `tests/test_validation.py` with 18 unit tests for validation functions
  (`require_config_keys`, `require_variables`, `require_input_file`, `is_enabled`).
- Fixed `LICENSE` formatting (GPL v3).
