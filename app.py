import os

from flask import Flask, jsonify, request
from pghbustime import BustimeAPI, Route

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
    limit = request.args.get('limit', 10)

    return jsonify({
        'stops': stop_locator.closest_stops(lat, lon, limit, rt)
    })

@app.route('/')
def hello():
    return ''

if __name__ == '__main__':
    app.run(debug=True)
