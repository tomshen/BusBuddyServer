import logging
import os

from flask import Flask, jsonify, request
from pghbustime import BustimeAPI, BustimeError, OfflineBus, Route, Stop

from stoplocator import StopLocator

try:
    bustime_api_key = os.environ['BUSTIME_API_KEY']
except:
    import secrets
    bustime_api_key = secrets.BUSTIME_API_KEY


app = Flask(__name__)

bustime = BustimeAPI(bustime_api_key)

stop_locator = StopLocator(bustime)


@app.route('/stops')
def stops():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    rt = request.args.get('rt')
    limit = int(request.args.get('limit', 10))

    return jsonify({
        'stops': stop_locator.closest_stops(lat, lon, limit, rt)
    })


@app.route('/stops/<stpid>')
def stop_routes(stpid=None):
    stop = Stop.get(bustime, stpid)
    try:
        def get_bus_stop(lat, lon, rt, direction):
            stop = stop_locator.current_stop(lat, lon, rt, direction)
            del stop['lat']
            del stop['lon']
            del stop['distance']
            del stop['routes']
            return stop

        predictions = [
            {
                'destination': pred.destination,
                'distance': pred.dist_to_stop / 5280.0,
                'dir': pred.direction,
                'eta': pred.eta.isoformat(),
                'lat': pred.bus.location[0],
                'lon': pred.bus.location[1],
                'rt': pred.route,
                'current_stop': get_bus_stop(
                    pred.bus.location[0],
                    pred.bus.location[1],
                    pred.route,
                    pred.direction)
            }
            for pred in stop.predictions()
            if type(pred.bus) is not OfflineBus
        ]
    except BustimeError as e:
        logging.error(e)
        predictions = []

    stop_info = stop_locator.get_stop_info(stop.id)
    return jsonify({
        'id': stop.id,
        'name': stop_info['stpnm'],
        'routes': stop_info['routes'],
        'predictions': predictions
    })


@app.route('/routes')
def routes():
    return jsonify({
        route['rt']: route for route in bustime.routes()['route']
    })


if __name__ == '__main__':
    app.run(debug=True)
