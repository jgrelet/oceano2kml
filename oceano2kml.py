#!/usr/bin/env python

# https://www.sigterritoires.fr/index.php/kml2-comment-creer-des-bulles-ballons-personnalisees/
# https://simplekml.readthedocs.io/en/latest/geometries.html
from netCDF4 import Dataset
import simplekml
import argparse
import toml
import os.path
import logging
from datetime import datetime

ELEVATION = 0
DEFAULT_OUTPUT_DIR = 'examples'
PROFILE_INSTRUMENTS = {
    'ctd': {
        'label': 'CTD Station',
        'count_label': 'stations',
        'color': simplekml.Color.red,
        'icon': 'http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png',
    },
    'ladcp': {
        'label': 'LADCP Profile',
        'count_label': 'profiles',
        'color': simplekml.Color.green,
        'icon': 'http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png',
    },
    'xbt': {
        'label': 'XBT Profile',
        'count_label': 'profiles',
        'color': simplekml.Color.azure,
        'icon': 'http://maps.google.com/mapfiles/kml/pushpin/wht-pushpin.png',
    },
}

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
        'python oceano2kml.py -t\n'
        'python oceano2kml.py -h\n'
        '\n',
        epilog='J. Grelet IRD US191 - Sep 2021 / Nov 2021')
    parser.add_argument('-d', '--debug', help='display debug information',
                        action='store_true')
    parser.add_argument('-t', '--time', help='display execution time',
                        action='store_true')
    parser.add_argument('-o', '--out', help="output directory, (default: %(default)s)",
                        default=DEFAULT_OUTPUT_DIR)
    parser.add_argument('-c', '--config', help="toml configuration file, (default: %(default)s)",
                        default='config.toml')
    return parser

def require_config_keys(cfg, keys, context='configuration'):
    missing = [key for key in keys if key not in cfg]
    if missing:
        raise ValueError("{} missing required key(s): {}".format(
            context, ', '.join(missing)))


def is_enabled(section):
    return section.get('file', 'none') != 'none'


def require_variables(dataset, names, file_path):
    missing = [name for name in names if name not in dataset.variables]
    if missing:
        raise ValueError("{} missing NetCDF variable(s): {}".format(
            file_path, ', '.join(missing)))


def require_input_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("Input file not found: {}".format(file_path))


def make_profile_style(options):
    style = simplekml.Style()
    style.iconstyle.color = options['color']
    style.iconstyle.scale = 1
    style.iconstyle.icon.href = options['icon']
    return style


def make_image_cdata(url, width):
    return '<![CDATA[\n<img src={} width={:d} />]]>'.format(url, width)


def add_profile_points(kml, cfg, instrument):
    section = cfg[instrument]
    options = PROFILE_INSTRUMENTS[instrument]
    require_config_keys(
        section, ['file', 'name', 'name_format', 'plots'], "[{}]".format(instrument))
    require_input_file(section['file'])

    print("{}: ".format(instrument.upper()), end='', flush=True)
    with Dataset(section['file'], mode='r') as dataset:
        require_variables(
            dataset,
            [cfg['profile'], cfg['longitude'], cfg['latitude']],
            section['file'])
        profiles = dataset.variables[cfg['profile']][:]
        longitude = dataset.variables[cfg['longitude']]
        latitude = dataset.variables[cfg['latitude']]
        style = make_profile_style(options)

        for i, profile in enumerate(profiles):
            url = section['plots'].format(profile)
            point = kml.newpoint()
            field_size = section['name_format']
            point.name = "{}{:{width}d}".format(
                section['name'], profile, width=field_size)
            point.description = "{}: {:05d}\n{}".format(
                options['label'], profile, make_image_cdata(url, 700))
            point.coords = [(longitude[i], latitude[i], ELEVATION)]
            point.altitudemode = simplekml.AltitudeMode.relativetoground
            point.style = style

    print("{} {}".format(len(profiles), options['count_label']))
    return len(profiles)


def add_tsg_track(kml, cfg):
    section = cfg['tsg']
    require_config_keys(section, ['file', 'params', 'plots'], '[tsg]')
    require_input_file(section['file'])

    print("TSG: ", end='', flush=True)
    with Dataset(section['file'], mode='r') as dataset:
        require_variables(
            dataset,
            [cfg['time'], cfg['longitude'], cfg['latitude']],
            section['file'])
        data = dataset.variables[cfg['time']][:]
        longitude = dataset.variables[cfg['longitude']]
        latitude = dataset.variables[cfg['latitude']]

        style = simplekml.Style()
        style.linestyle.color = simplekml.Color.blue
        style.linestyle.width = 3

        linestring = kml.newlinestring()
        linestring.name = f"TSG - {section['params']}"
        linestring.description = make_image_cdata(section['plots'], 500)
        linestring.style = style

        for i in range(0, len(data)):
            linestring.coords.addcoordinates([(longitude[i], latitude[i])])

    print("{} data".format(len(data)))
    return len(data)


def output_path(output_dir, cruise):
    path = output_dir
    if path == '.':
        path = os.getcwd()
    return os.path.normpath(os.path.join(path, '{}.kml'.format(cruise.lower())))


def main():
    start_time = datetime.now()
    parser = processArgs()
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

    cfg = toml.load(args.config)
    logging.debug(cfg)
    require_config_keys(
        cfg, ['cruise', 'time', 'latitude', 'longitude', 'profile'])

    kml = simplekml.Kml()
    feature_count = 0

    for instrument in PROFILE_INSTRUMENTS:
        if instrument in cfg and is_enabled(cfg[instrument]):
            feature_count += add_profile_points(kml, cfg, instrument)

    if 'tsg' in cfg and is_enabled(cfg['tsg']):
        feature_count += add_tsg_track(kml, cfg)

    if feature_count == 0:
        raise ValueError('No enabled instrument found in configuration')

    dest = output_path(args.out, cfg['cruise'])
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    kml.save(dest)
    print("File {} saved".format(dest))
    logging.debug(kml.kml())

    if args.time:
        print('Duration: {}'.format(datetime.now() - start_time))


if __name__ == "__main__":
    main()
