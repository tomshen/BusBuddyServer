import os

from flask import Flask, jsonify
from pghbustime import BustimeAPI, Route

try:
    bustime_api_key = os.environ['BUSTIME_API_KEY']
except:
    import secrets
    bustime_api_key = secrets.BUSTIME_API_KEY

app = Flask(__name__)
bustime = BustimeAPI(bustime_api_key)

@app.route('/')
def hello():
    route_71b = Route.get(bustime, '71B')
    return jsonify({ 'buses': [
        str(bus) for bus in route_71b.busses] })

if __name__ == '__main__':
    app.run(debug=True)