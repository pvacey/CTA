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


def getStationId(name, line):
    stations = requests.get(
        'https://data.cityofchicago.org/resource/8mj8-j3c4.json').json()
    resp = ''
    for s in stations:
        # station_descriptive_name, station_name, stop_id, stop_name
        l, name, sID = s[line], s['stop_name'], s["stop_id"]
        # import pdb; pdb.set_trace()
        if l == True:
            resp += "{} {}{}".format(sID, name, '\n')
            # print s['stop_name']
    print resp


def getLines():
    return {'Red': 'Red', 'Blue': 'Blue', 'G': 'Green', 'Brn': 'Brown',
            'P': 'Purple', 'Y': 'Yellow', 'Pnk': 'Pink', 'O': 'Orange'}


def getArrivals(api_key, station_id):
    return requests.get(
        'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&mapid={}&max=20&outputType=JSON'.format(api_key, station_id)).json()

# Station IDs http://www.transitchicago.com/developers/ttdocs/default.aspx#_Toc296199909
# 40090 - Damen Brownline
# 40160 - LaSalle/Van Buren
# 40460 - Mechandise Mart

# def my_stops():
#     resp = '-' * 31
#     resp += '\n'
#     resp += '| CTA Brownline' + ' ' * 15 + '|\n'
#     resp += '-' * 31
#     resp += '\n'
#     resp += printNextArrivals('40090', 'Brn', 'Loop')
#     resp += '\n\n'
#     resp += printNextArrivals('40460', 'Brn', 'Kimball')
#     resp += '\n'
#     resp += '-' * 31
#     return resp


if __name__ == "__main__":
    # getStationId('18th', 'blue')
    print printNextArrivals('40590', 'Blue', 'O;Hare')
