#!venv/bin/python
"""An efficient way to check your train schedule."""
import json
from datetime import datetime
import sys
import yaml
import requests

def get_raw_stations():
    """Gets the raw station information"""
    return requests.get('https://data.cityofchicago.org/resource/8mj8-j3c4.json').json()

def get_line_id(line_name):
    lines = get_lines()
    for key in lines.keys():
        if line_name.lower() == key.lower():
            return lines[key]
    raise ValueError('Line not found: {}'.format(line_name))

def get_lines():
    """Returns CTA Format of thier Line for API"""
    return {
        'red':'Red',
        'blue':'Blue',
        'green':'G',
        'brown':'Brn',
        'purple':'P',
        'yellow':'Y',
        'pink':'Pnk',
        'orange':'O'
    }

def get_line_stops(req_line):
    """Returns a list of stops for a given line"""
    line_id = get_line_id(req_line).lower()
    if not line_id:
        raise ValueError('Line not found: {}'.format(req_line))
    raw_stops = get_raw_stations()
    stops = []
    for stop in raw_stops:
        if stop[line_id]:
            stops.append(stop)
    return stops

def get_raw_line_station_names(req_line):
    """Returns a list of station names for a given line"""
    stops = get_line_stops(req_line)
    names = []
    [names.append(tmp['station_name']) for tmp in stops]
    # return a deduped list, each station has two stops
    return list(set(names))

def get_raw_arrivals(line_name,station_name):
    """Returns upcoming arrivals for a given station and line"""
    line_name = line_name.lower()
    station_name = station_name.lower()
    raw_stops = get_line_stops(line_name)
    # find stop by matching name
    station_id = False
    for stop in raw_stops:
        if station_name == stop['station_name'].lower():
            station_id = stop['map_id']
            break

    if not station_id:
        raise ValueError('station not found: {}'.format(station_name))
    # load API key
    with open("config.yml", 'r') as yml:
        cfg = yaml.load(yml)
    api_key = cfg['api']['key']

    # this will have all lines for a particular station
    raw_arrivals = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&mapid={}&max=20&outputType=JSON'
        .format(api_key, station_id)).json()

    # filter out arrivals for trains of a different line color
    line_id = get_line_id(line_name)
    # orange line is the only one that uses a different ID here than the other API
    if line_id == 'O': line_id = 'Org'
    arrivals = []
    for arrival in raw_arrivals['ctatt']['eta']:
        if arrival['rt'] == line_id:
            arrivals.append(arrival)

    return arrivals

def get_term_lines():
    raw_lines = get_lines()
    resp = '-' * 35
    resp += '\n'
    resp += 'CTA TRAIN LINES\n'
    resp += '-' * 35
    for line in raw_lines.keys():
        resp += '\n + {}'.format(line)
    resp += '\n'
    return resp

def get_term_line_stations(line_name):
    stations = get_raw_line_station_names(line_name)
    resp = '-' * 35
    resp += '\nCTA {} LINE STATIONS\n'.format(line_name.upper())
    resp += '-' * 35
    for sta in stations:
        resp += '\n + {}'.format(sta)
    resp += '\n'
    resp += '-' * 35
    resp += '\n'
    return resp

def get_term_arrivals(line_name, station_name):

    header = 'CTA {} LINE @ {}'.format(line_name.upper(), station_name.upper())
    resp = '-' * 35
    resp += '\n'
    resp += header + '\n'
    resp += '-' * 35

    # build a dictionary of arrival strings
    # if this raises an error for the station not existing, return the list
    # of stations to the user instead
    try:
        raw_arrivals = get_raw_arrivals(line_name=line_name, station_name=station_name)
    except ValueError:
        return get_term_line_stations(line_name)
    json.dumps(raw_arrivals)

    stops = {}
    for raw_arrival in raw_arrivals:
        dest = raw_arrival['destNm']
        if dest not in stops.keys():
            stops[dest] = []
        # build a string for each arrival
        t = datetime.strptime(raw_arrival['arrT'], "%Y-%m-%dT%H:%M:%S")
        time = t.strftime("%I:%M:%S")
        elapsed = (t - datetime.now()).seconds
        minutes = elapsed / 60
        seconds = elapsed % 60
        tmp = '\n - {}m {}s from now ({})'.format(minutes, seconds, time)
        stops[dest].append(tmp)

    for dest,arrivals in stops.items():
        resp += '\n{} ---> {}'.format(raw_arrivals[0]['staNm'], dest)
        for a in arrivals:
            resp += a

    resp += '\n'
    resp += '-' * 35
    resp += '\n'
    return resp


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print 'usage:\n  ./cta.py <line>'
        print '  ./cta.py <lime> <station_name>'
        print 'examples:\n  ./cta.py brown'
        print '  ./cta.py blue lasalle\n'
        print get_term_lines()
        exit(1)

    if len(sys.argv) == 2:
        print get_term_line_stations(sys.argv[1])

    if len(sys.argv) == 3:
        print get_term_arrivals(line_name=sys.argv[1], station_name=sys.argv[2])
