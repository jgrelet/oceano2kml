# oceano2kml [![Build Status](https://travis-ci.com/jgrelet/oceano2kml.svg?branch=master)](https://app.travis-ci.com/github/jgrelet/oceano2kml)

This program is the Python and updated version of the Golang cruiseTrack2kml.
oceano2kml is used for rendering oceanographic data, CTD, XBT profiles and TSG (thermosalinograph) plots to Google Earth Keyhole Markup Language (KML) files.

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
```
