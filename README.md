# oceano2kml
This program is the Python and updated version of the Golang cruiseTrk2oceano.
oceano2kml is used for rendering oceanographic data, CTD, XBT profiles and TSG (thermosalinograph) plots to Google Earth Keyhole Markup Language (KML) files.
The input file format is in NetCDF OceanSITES and the configuration is described in a TOML file.
This version is written in Python 3 and manages profile and trajectory data. 
The reading of time-series files as well as ASCII files will be developed with the fileExtractor module in a future version.

## usage

'''bash
python oceano2kml.py 
python oceano2kml.py -c config.toml
python oceano2kml.py -c config.toml -d
'''
