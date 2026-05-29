# oceano2kml [![CI](https://github.com/jgrelet/oceano2kml/actions/workflows/ci.yml/badge.svg)](https://github.com/jgrelet/oceano2kml/actions/workflows/ci.yml)

This program is the Python and updated version of the Golang cruiseTrack2kml.
oceano2kml is used for rendering oceanographic data, CTD, LADCP, XBT profiles
and TSG (thermosalinograph) plots to Google Earth Keyhole Markup Language
(KML) files.

The input file format is in NetCDF OceanSITES and the configuration is described in a TOML file.
This version is written in Python3 and manages profile and trajectory data.

## Installation

Install mamba first. The recommended option is Miniforge, which provides
`mamba` and conda-forge by default:

```sh
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
```

If conda is already installed, mamba can also be installed in the base
environment:

```sh
conda install -n base -c conda-forge mamba
```

Create the environment with mamba:

```sh
mamba env create -f environment.yml
mamba activate oceano2kml
```

Update the environment after dependency changes:

```sh
mamba env update -n oceano2kml -f environment.yml --prune
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
python -m py_compile oceano2kml.py
python -m unittest discover -s tests -v
python oceano2kml.py -c pirata-fr31.toml -o /tmp/oceano2kml-check
python oceano2kml.py -c amazomix.toml -o /tmp/oceano2kml-check
```

## Continuous integration

GitHub Actions workflows are stored in `.github/workflows/`.

- `ci.yml` runs on pushes, pull requests, and manual dispatch. It creates the
  Python 3.11 mamba environment, compiles the script, runs the regression tests, and
  generates the bundled examples.
- `release.yml` runs on tags matching `v*` or by manual dispatch with a tag. It
  runs the checks, builds a ZIP archive, and creates a GitHub release.
