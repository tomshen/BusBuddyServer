import json
import os.path

import geopy
import geopy.distance as geodistance

class StopLocator(object):
    def __init__(self, bustime, stops_file='stops.json'):
        if os.path.isfile(stops_file):
            with open(stops_file) as stops_fp:
                stops = json.load(stops_fp)
                self.stops = stops
        else:
            self.download_stops(bustime)

        for stop in self.stops.values():
            stop['point'] = geopy.Point(stop['lat'], stop['lon'])


    def download_stops(self, bustime):
        self.stops = {}
        for route in bustime.routes()['route']:
            rt = route['rt']
            for direction in ['INBOUND', 'OUTBOUND']:
                for stop in bustime.stops(rt, direction)['stop']:
                    if stop['stpid'] not in self.stops:
                        stop['routes'] = { rt: direction }
                        self.stops[stop['stpid']] = stop
                    else:
                        self.stops[stop['stpid']]['routes'][rt] = direction


        with open('stops.json', 'w') as stops_fp:
            json.dump(self.stops, stops_fp, sort_keys=True, indent=2)


    def closest_stops(self, lat, lon, limit=10, rt=None):
        valid_stops = []
        origin = geopy.Point(lat, lon)

        for stop in self.stops.values():
            if not rt or rt in stop['routes']:
                stop = stop.copy()
                stop['distance'] = geodistance.distance(origin, stop['point']).mi
                del stop['point']
                valid_stops.append(stop)

        return sorted(valid_stops,
            key=lambda stop: stop['distance'])[:limit]

    def get_stop_info(self, stpid):
        return next((stop for sid, stop in self.stops.items()
            if sid == stpid), None)
