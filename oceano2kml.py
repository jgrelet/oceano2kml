#!/usr/bin/env python

# https://www.sigterritoires.fr/index.php/kml2-comment-creer-des-bulles-ballons-personnalisees/
# https://simplekml.readthedocs.io/en/latest/geometries.html
from netCDF4 import Dataset
import simplekml
from configparser import ConfigParser
import argparse
import toml
import os.path
import logging
from datetime import datetime

elevation = 0
path = 'examples'  # default path where to write result kml file

def processArgs():
    parser = argparse.ArgumentParser(
        description="This program reads several ASCII or NetCDF files and creates a KML file \
            for Google Earth to display the ship's route and station positions. \
            Each element is clickable to display surface temperature/salinity data, \
            vertical profiles of CTD, LADCP and XBT stations.",

        usage='\npython oceano2kml.py\n'
        'python oceano2kml.py -c <config.toml>\n'
        'python oceano2kml.py -c <config.toml> -o <dir>\n'
        'python oceano2kml.py -d\n'
        'python oceano2kml.py -h\n'
        '\n',
        epilog='J. Grelet IRD US191 - Sep 2021 / Nov 2021')
    parser.add_argument('-d', '--debug', help='display debug informations',
                        action='store_true')
    parser.add_argument('-t', '--time', help='display execution time',
                        action='store_true')
    parser.add_argument('-o', '--out', help="output directory, (default: %(default)s)",
                        default='examples')
    parser.add_argument('-c', '--config', help="toml configuration file, (default: %(default)s)",
                        default='config.toml')
    return parser

if __name__ == "__main__":
    '''
    usage:
    > python oceano2kml.py 
    > python oceano2kml.py -c <config.toml>
    '''
    start_time = datetime.now()

    # recover and process line arguments
    parser = processArgs()
    args = parser.parse_args()

    # set looging mode if debug
    if args.debug:
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # read config Toml file and get the physical parameter list (Roscop code) for the specified instrument
    cfg = toml.load(args.config)
    logging.debug(cfg)

    # CTD
    if cfg['ctd']['file'] != 'none':
        print("CTD: ", end = '', flush=True)
        ctd = Dataset(cfg['ctd']['file'], mode='r')
        profiles = ctd.variables[cfg['profile']][:]
        ctd_url = cfg['ctd']['plots']

        kml = simplekml.Kml()
        style = simplekml.Style()
        style.iconstyle.color = simplekml.Color.red  # Make the icon red
        style.iconstyle.scale = 1
        style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png'
        #style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

        # plot CTD station icons red
        for i in range(0, len(profiles)):    
            url = ctd_url.format(profiles[i]) 
            cdata = '<![CDATA[\n<img src={} width={:d} />]]>'.format(url, 700)     
            point = kml.newpoint()
            field_size = cfg['ctd']['name_format']
            point.name="{}{:{witdh}d}".format(cfg['ctd']['name'], profiles[i], witdh=field_size)
            point.description = "CTD Station: {:05d}\n{}".format(profiles[i], cdata)
            point.coords=[(ctd.variables[cfg['longitude']][i], ctd.variables[cfg['latitude']][i], elevation)]
            point.altitudemode = simplekml.AltitudeMode.relativetoground 
            point.style = style
        print("{} stations".format(len(profiles)))
        ctd.close()

    # XBT
    if cfg['xbt']['file'] != 'none':
        print("XBT: ", end = '', flush=True)
        xbt = Dataset(cfg['xbt']['file'], mode='r')
        profiles = xbt.variables[cfg['profile']][:]
        xbt_url = cfg['xbt']['plots']

        # plot XBT profiles icons green
        style = simplekml.Style()
        style.iconstyle.color = simplekml.Color.azure  # Make the icon green

        for i in range(0, len(profiles)):    
            url = xbt_url.format(profiles[i]) 
            cdata = '<![CDATA[\n<img src={} width={:d} />]]>'.format(url, 700)     
            point = kml.newpoint()
            field_size = cfg['xbt']['name_format']
            point.name='{}{:{witdh}d}'.format(cfg['xbt']['name'], profiles[i], witdh=field_size)
            point.description = "XBT Profile: {:05d}\n{}".format(profiles[i], cdata)
            point.coords=[(xbt.variables[cfg['longitude']][i], xbt.variables[cfg['latitude']][i], elevation)]
            point.altitudemode = simplekml.AltitudeMode.relativetoground 
            point.style = style
        print("{} profiles".format(len(profiles)))
        xbt.close()

    # TSG
    if cfg['tsg']['file'] != 'none':
        print("TSG: ", end = '',flush=True)
        tsg = Dataset(cfg['tsg']['file'], mode='r')
        data = tsg.variables[cfg['time']][:]
        tsg_url = cfg['tsg']['plots']

        # plot TSG data as lineString in blue
        style = simplekml.Style()
        style.linestyle.color = simplekml.Color.blue  # Make the line blue
        style.linestyle.width = 3
        cdata = '<![CDATA[\n<img src={} width={:d} />]]>'.format(tsg_url, 500)     
        ls = kml.newlinestring()
        ls.name = f"TSG - {cfg['tsg']['params']}"
        ls.description = cdata
        #ls.altitudemode = simplekml.AltitudeMode.relativetoground 
        ls.style = style

        for i in range(0, len(data)):    
            ls.coords.addcoordinates([(tsg.variables[cfg['longitude']][i], 
                tsg.variables[cfg['latitude']][i])])
        print("{} data".format(len(data)))
        tsg.close()

    # save kml file to the right directory
    cruise = cfg['cruise'].lower()
    file_name = f'{cruise}.kml'
    if args.out :
        path = args.out
    if path == '.':         # os.path.join failed with path = '.' !
        path = os.getcwd()
    dest = os.path.normpath(os.path.join(path, file_name))
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    kml.save(dest)
    print("File {} saved".format(dest))
    logging.debug(kml.kml())

    # display execution elasped time
    if args.time:
        print('Duration: {}'.format(datetime.now() - start_time))
    
  
    

