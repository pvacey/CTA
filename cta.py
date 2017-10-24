#!venv/bin/python
import requests
import json
from datetime import datetime
import ConfigParser
import yaml

def printNextArrivals(station_id, line, dest):
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    api_key =  cfg['api']['key']
    # Red, Blue, G, Brn, P, Y Pnk, O
    lines = getLines()
    try:
        resp = getArrivals(api_key, station_id)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print e
        sys.exit(1)
    arrivals = []
    trains = resp['ctatt']['eta']
    for t in trains:
        if t['rt'] == line and t['destNm'] == dest:
            tmp = datetime.strptime(t['arrT'], "%Y-%m-%dT%H:%M:%S")
            arrival = tmp.strftime("%I:%M:%S")
            elapsed = (tmp - datetime.now()).seconds
            minutes = elapsed / 60
            seconds = elapsed % 60

            arrivals.append({'time': arrival,
                             'minutes': minutes,
                             'seconds': seconds})
            station_name = t['staNm']

    response = '-' * 31
    response += '\n'
    response += '| CTA {} Line'.format(lines[line]) + ' ' * 15 + '|\n'
    response += '-' * 31
    response += '\n'
    response += '{} ---> {}'.format(station_name, dest)
    for a in arrivals:
        response += '\n - {}m {}s from now ({})'.format(
            a['minutes'], a['seconds'], a['time'])
    response += '\n'
    response += '-' * 31
    return response


def get_lines():
    return {'red': 'Red', 'Blue': 'Blue', 'G': 'Green', 'Brn': 'Brown',
    'P': 'Purple', 'Y': 'Yellow', 'Pnk': 'Pink', 'O': 'Orange'}

def get_raw_stations():
    return requests.get('https://data.cityofchicago.org/resource/8mj8-j3c4.json').json()

def get_stops(line):
    '''Returns list of stops for a given line'''
    tmp = get_lines()
    new_lines = dict(zip(tmp.values(), tmp.keys()))
    station_code = new_lines[line].lower()
    stations = get_raw_stations()
    resp = []
    for s in stations:
        line_flag, stop_name, stop_id = s[station_code], s['stop_name'], s['stop_id']
        if line_flag:
            resp.append({'stop_id':stop_id, 'stop_name':stop_name,})
    return resp

def get_station(station_id):
    '''to-do'''
    return

def get_arrivals_stop(api_key, station_id):
    return requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&stpid={}&max=20&outputType=JSON'.format(api_key, station_id)).json()


if __name__ == "__main__":
    # setup - grab api key from config file
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    api_key =  cfg['api']['key']

    stops = get_stops('Pink')
    for s in stops:
        print s

# Station IDs http://www.transitchicago.com/developers/ttdocs/default.aspx#_Toc296199909
