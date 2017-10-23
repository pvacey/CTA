<<<<<<< HEAD
# CTA
Simple script to display CTA Train arrival times.

```
-------------------------------
| CTA Brownline               |
-------------------------------
Damen ---> Loop
 - 0m 30s from now (10:07:41)
 - 11m 51s from now (10:19:02)

Merchandise Mart ---> Kimball
 - 12m 25s from now (10:19:36)
 - 24m 51s from now (10:32:02)
-------------------------------
```

## Getting Started
This assumes you will be using `virtualenv` to create a local python environment to run this code.
1. `virtualenv venv`
2. `venv/bin/pip install -r requirements.txt`
3. supply your own API key in `cta.py`
4. `./gunicorn.sh debug` to start the webui on port 8002 or `python -c "import cta; print cta.my_stops()"` for cli output

=======
# CTA Train Tracker [![Build Status](https://travis-ci.org/dancigrang/CTA.svg?branch=master)](https://travis-ci.org/dancigrang/CTA)
>>>>>>> 0626747b47f97573be267c0a0d0cd170a86640f4
