# oceano2kml [![Build Status](https://app.travis-ci.com/jgrelet/oceano2kml.svg?branch=main)](https://app.travis-ci.com/github/jgrelet/oceano2kml)

This program is the Python and updated version of the Golang cruiseTrack2kml.
oceano2kml is used for rendering oceanographic data, CTD, LADCP, XBT profiles
and TSG (thermosalinograph) plots to Google Earth Keyhole Markup Language
(KML) files.

The input file format is in NetCDF OceanSITES and the configuration is described in a TOML file.
This version is written in Python3 and manages profile and trajectory data.

## Installation

Create virtual env with conda, ex:

```sh
conda create -n oceano2kml python=3.9
conda activate oceano2kml 
```

Install all mandatory modules:

```sh
conda install -c conda-forge netCDF4 simplekml toml 
```

## Usage

```bash
python oceano2kml.py -h
python oceano2kml.py -c <config.toml>
python oceano2kml.py -c <config.toml> -d
python oceano2kml.py -c <config.toml> -o <output-dir>
python oceano2kml.py -c <config.toml> -t
```

Examples:

```bash
python oceano2kml.py -c pirata-fr31.toml
python oceano2kml.py -c amazomix.toml -o /tmp/oceano2kml-check
```

By default, generated KML files are written to `examples/`. The output file name
is built from the lower-case `cruise` value in the TOML configuration.

## Configuration

The TOML file defines common NetCDF variable names and one section per
instrument. Supported profile instruments are `[ctd]`, `[ladcp]`, and `[xbt]`.
The `[tsg]` section is rendered as a KML line string.

Required global keys:

```toml
cruise = "AMAZOMIX"
time = "TIME"
latitude = "LATITUDE"
longitude = "LONGITUDE"
profile = "PROFILE"
```

Profile sections require:

```toml
[ctd]
file = "data/amazomix/OS_AMAZOMIX_CTD.nc"
name = "St"
name_format = 5
plots = "http://example.org/plot-{:05d}.png"
```

Set `file = "none"` to disable an instrument section.

## Validation

Run a syntax check and generate the bundled examples into a temporary directory:

```bash
python3 -m py_compile oceano2kml.py
python3 -m unittest discover -s tests -v
python3 oceano2kml.py -c pirata-fr31.toml -o /tmp/oceano2kml-check
python3 oceano2kml.py -c amazomix.toml -o /tmp/oceano2kml-check
```

## Continuous integration

GitHub Actions workflows are stored in `.github/workflows/`.

- `ci.yml` runs on pushes, pull requests, and manual dispatch. It installs the
  Python dependencies, compiles the script, runs the regression tests, and
  generates the bundled examples.
- `release.yml` runs on tags matching `v*` or by manual dispatch with a tag. It
  runs the checks, builds a ZIP archive, and creates a GitHub release.
