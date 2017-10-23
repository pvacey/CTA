import falcon
import json
import datetime
import cta

class PrintStops:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.body = cta.my_stops()

api = falcon.API()
api.add_route('/', PrintStops())
