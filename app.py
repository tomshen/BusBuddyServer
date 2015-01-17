import os

from flask import Flask, jsonify, request
from pghbustime import BustimeAPI, OfflineBus, Route, Stop

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
        predictions = [
            {
                'destination': pred.destination,
                'distance': pred.dist_to_stop / 5280.0,
                'dir': pred.direction,
                'eta': pred.eta,
                'lat': pred.bus.location[0],
                'lon': pred.bus.location[1],
                'rt': pred.route,
                'current_stop': (stop_locator.closest_stops(
                    pred.bus.location[0],
                    pred.bus.location[1],
                    1,
                    pred.route) or [None])[0] # I know this is awful
            }
            for pred in stop.predictions()
            if type(pred.bus) is not OfflineBus
        ]
    except:
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
