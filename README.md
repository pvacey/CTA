# CTA Train Tracker [![Build Status](https://travis-ci.org/dancigrang/CTA.svg?branch=master)](https://travis-ci.org/pvacey/CTA) [![BCH compliance](https://bettercodehub.com/edge/badge/pvacey/CTA?branch=master)](https://bettercodehub.com/)

Simple script to display CTA Train arrival times.

## Usage
The script can be run directly by executing `cta.py` or as an HTTP server by running `application.py` and using `curl` as a client. 


## Get a list of arrival times by line and station
Direct: `./cta.py blue damen`

Web `curl localhost:5000/blue/damen`
```
-----------------------------------
CTA BLUE LINE @ DAMEN
-----------------------------------
Damen ---> O'Hare
 - 0m 6s from now (05:38:56)
 - 13m 46s from now (05:52:36)
 - 15m 56s from now (05:54:46)
Damen ---> Forest Park
 - 3m 43s from now (05:42:33)
 - 12m 41s from now (05:51:31)
 - 16m 42s from now (05:55:32)
-----------------------------------
```

### Get a list of train stations by line
Direct: `./cta.py blue`

Web: `curl localhost:5000/blue`
```
-----------------------------------
CTA BLUE LINE STATIONS
-----------------------------------
 + Addison
 + Austin
 + Belmont
 + California
 + Chicago
 + Cicero
 + Clark/Lake
 + Clinton
 + Cumberland
 + Damen
 + Division
 + Forest Park
 + Grand
 + Harlem
 + Illinois Medical District
 + Irving Park
 + Jackson
 + Jefferson Park
 + Kedzie-Homan
 + LaSalle
 + Logan Square
 + Monroe
 + Montrose
 + O'Hare
 + Oak Park
 + Pulaski
 + Racine
 + Rosemont
 + UIC-Halsted
 + Washington
 + Western
-----------------------------------
```

### Get a list of train lines
Direct: `.cta.py`

Web: `curl localhost:5000/`
```
-----------------------------------
CTA TRAIN LINES
-----------------------------------
 + Blue
 + Brown
 + Green
 + Orange
 + Pink
 + Purple
 + Red
 + Yellow
```
