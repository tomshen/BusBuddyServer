import json
import os.path

import geopy
import geopy.distance as geodistance
from pghbustime import Route

class StopLocator(object):
    def __init__(self, bustime, stops_file='stops.json'):
        if os.path.isfile(stops_file):
            with open(stops_file) as stops_fp:
                stops = json.load(stops_fp)
                self.stops = stops
        else:
            self.download_stops(bustime)

        for stop in self.stops:
            stop['point'] = geopy.Point(stop['lat'], stop['lon'])


    def download_stops(self, bustime):
        stpids = set()
        self.stops = []
        for route in bustime.routes()['route']:
            rt = route['rt']
            for direction in ['INBOUND', 'OUTBOUND']:
                for stop in bustime.stops(rt, direction)['stop']:
                    if stop['stpid'] not in stpids:
                        stpids.add(stop['stpid'])
                        stop['dir'] = direction
                        stop['rt'] = rt
                        self.stops.append(stop)

        with open('stops.json', 'w') as stops_fp:
            json.dump(self.stops, stops_fp, sort_keys=True, indent=2)


    def stops_within(self, lat, lon, max_dist, rt=None):
        near_stops = []
        origin = geopy.Point(lat, lon)
        for stop in self.stops:
            dist = geodistance.distance(origin, stop['point']).mi
            if dist < max_dist:
                if not rt or stop['rt'] == rt:
                    stop = stop.copy()
                    del stop['point']
                    stop['distance'] = dist
                    near_stops.append(stop)
        return sorted(near_stops, key=lambda stop: stop['distance'])


    def closest_stops(self, lat, lon, limit=10, rt=None):
        dist = 0.5
        stops = self.stops_within(lat, lon, dist, rt)
        while len(stops) < 5:
            dist *= 2
            stops = self.stops_within(lat, lon, dist, rt)
        return stops[:limit]
