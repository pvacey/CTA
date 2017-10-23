#!venv/bin/python
import requests
import json
from datetime import datetime
import ConfigParser


def printNextArrivals(station_id, line, dest):
    api_key='insert key here'
    resp = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&mapid={}&max=20&outputType=JSON'.format(api_key,station_id)).json()
    arrivals = []
    trains = resp['ctatt']['eta']
    for t in trains:
        if t['rt'] == line and t['destNm'] == dest:
            tmp = datetime.strptime(t['arrT'],"%Y-%m-%dT%H:%M:%S")
            arrival = tmp.strftime("%I:%M:%S")
            elapsed = (tmp - datetime.now()).seconds
            minutes = elapsed / 60
            seconds = elapsed % 60

            arrivals.append({'time':arrival,
                             'minutes':minutes,
                             'seconds':seconds})
            station_name = t['staNm']

    response = '{} ---> {}'.format(station_name,dest)
    for a in arrivals:
        response += '\n - {}m {}s from now ({})'.format(a['minutes'],a['seconds'],a['time'])
    return response


# Station IDs http://www.transitchicago.com/developers/ttdocs/default.aspx#_Toc296199909
# 40090 - Damen Brownline
# 40160 - LaSalle/Van Buren
# 40460 - Mechandise Mart

def my_stops():
    resp = '-------------------------------'
    resp += '\n| CTA Brownline               |\n'
    resp += '-------------------------------'
    resp += '\n'
    resp += printNextArrivals('40090', 'Brn', 'Loop')
    resp += '\n\n'
    resp += printNextArrivals('40460', 'Brn', 'Kimball')
    resp += '\n-------------------------------'
    return resp
