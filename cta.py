#!venv/bin/python
"""An efficient way to check your train schedule."""
# import json
from datetime import datetime
import sys
import yaml
import requests


def print_next_arrivals(station_id, line, dest):
    """Prints the arrivals from the station provided"""
    with open("config.yml", 'r') as yml:
        cfg = yaml.load(yml)

    api_key = cfg['api']['key']
    # Red, Blue, G, Brn, P, Y Pnk, O
    lines = get_lines()
    try:
        resp = get_arrivals_stop(api_key, station_id)
    except requests.exceptions.RequestException as error:  # This is the correct syntax
        print error
        sys.exit(1)
    arrivals = []
    trains = resp['ctatt']['eta']
    for train in trains:
        if train['rt'] == line and train['destNm'] == dest:
            tmp = datetime.strptime(train['arrT'], "%Y-%m-%dT%H:%M:%S")
            arrival = tmp.strftime("%I:%M:%S")
            elapsed = (tmp - datetime.now()).seconds
            minutes = elapsed / 60
            seconds = elapsed % 60

            arrivals.append({'time': arrival,
                             'minutes': minutes,
                             'seconds': seconds})
            station_name = train['staNm']

    response = '-' * 31
    response += '\n'
    response += '| CTA <span class="{}">{}</span> Line'.format(lines[line].lower(),lines[line]) + ' ' * 15 + '|\n'
    response += '-' * 31
    response += '\n'
    response += '{} ---> {}'.format(station_name, dest)
    for arrival in arrivals:
        response += '\n - {}m {}s from now ({})'.format(
            arrival['minutes'], arrival['seconds'], arrival['time'])
    response += '\n'
    response += '-' * 31
    return response


def get_lines():
    """Returns CTA Format of thier Line for API"""
    return {'red': 'Red', 'Blue': 'Blue', 'G': 'Green', 'Brn': 'Brown',
            'P': 'Purple', 'Y': 'Yellow', 'Pnk': 'Pink', 'O': 'Orange'}

def get_raw_stations():
    """Gets the raw station information"""
    return requests.get('https://data.cityofchicago.org/resource/8mj8-j3c4.json').json()

def get_stops(line):
    '''Returns list of stops for a given line'''
    tmp = get_lines()
    new_lines = dict(zip(tmp.values(), tmp.keys()))
    station_code = new_lines[line].lower()
    stations = get_raw_stations()
    resp = []
    for station in stations:
        line_flag, stop_name, stop_id = station[station_code], station['stop_name'], station['stop_id']
        if line_flag:
            resp.append({'stop_id':stop_id, 'stop_name':stop_name,})
    return resp

def get_station(station_id):
    '''to-do'''
    return station_id

def get_arrivals_stop(api_key, station_id):
    """Pulls from API to get arrival stops"""
    return requests.get(
        'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&stpid={}&max=20&outputType=JSON'
        .format(api_key, station_id)).json()


if __name__ == "__main__":
    # setup - grab api key from config file
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    api_key = cfg['api']['key']

    stops = get_stops('Blue')
    for s in stops:
        print s

# Station IDs http://www.transitchicago.com/developers/ttdocs/default.aspx#_Toc296199909
