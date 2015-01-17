# BusBuddyServer

Requires Python 2.7

## API

### GET `/routes`

#### Response
```javascript
{
  "1": {
    "rt": "1", // route id
    "rtclr": "#3300cc", // route color
    "rtnm": "FREEPORT ROAD" // route name
  }, 
  "12": {
    "rt": "12", 
    "rtclr": "#cc00cc", 
    "rtnm": "MCKNIGHT"
  }, 
  .
  .
  .
}
```

### GET `/stops`

#### Request

* `lat`: current location latitude
* `lon`: current location longitude
* `limit` (optional): number of stops to retrieve
* `rt` (optional): limit to stops for this route

#### Response

```javascript
// /stops?lat=40.450402&lon=-79.932811&limit=10
{
  "stops": [
    {
      "distance": 0.1001644210848218, 
      "lat": "40.448971513954", 
      "lon": "-79.932487500001", 
      "routes": {
        "71B": "INBOUND", 
        "71D": "INBOUND"
      }, 
      "stpid": "3144", 
      "stpnm": "5th Ave at Bellefonte St"
    }, 
    {
      "distance": 0.10600817314439809, 
      "lat": "40.448874022701", 
      "lon": "-79.932601073413", 
      "routes": {
        "71B": "OUTBOUND", 
        "71D": "OUTBOUND"
      }, 
      "stpid": "3256", 
      "stpnm": "5th Ave opp Bellefonte St"
    }, 
    {
      "distance": 0.13272244473225814, 
      "lat": "40.451258189964", 
      "lon": "-79.930556246032", 
      "routes": {
        "64": "OUTBOUND"
      }, 
      "stpid": "15451", 
      "stpnm": "Negley Ave at Howe St"
    }, 
    {
      "distance": 0.1378829957684234, 
      "lat": "40.451124008543", 
      "lon": "-79.930371864419", 
      "routes": {
        "64": "INBOUND"
      }, 
      "stpid": "11087", 
      "stpnm": "Negley Ave at Howe St"
    }, 
    {
      "distance": 0.141689688469219, 
      "lat": "40.450573150845", 
      "lon": "-79.930132302248", 
      "routes": {
        "64": "OUTBOUND"
      }, 
      "stpid": "15452", 
      "stpnm": "Negley Ave at Kentkucky Ave"
    }
  ]
}
```

### GET `/stops/<stpid>`
```javascript
// /stops/7117
{
  "id": "7117", 
  "name": "Forbes Ave opp Morewood Ave", 
  "predictions": [
    {
      "current_stop": {
        "stpid": "30", 
        "stpnm": "Forbes Ave past Bouquet St"
      }, 
      "destination": "McKeesport", 
      "dir": "OUTBOUND", 
      "distance": 0.7426136363636363, 
      "eta": "Sat, 17 Jan 2015 17:02:27 GMT", 
      "lat": 40.44234216863459, 
      "lon": -79.95583995472302, 
      "rt": "61C"
    }, 
    {
      "current_stop": {
        "stpid": "3242", 
        "stpnm": "Forbes Ave at McAnulty Dr"
      }, 
      "destination": "North Braddock", 
      "dir": "OUTBOUND", 
      "distance": 2.7738636363636364, 
      "eta": "Sat, 17 Jan 2015 17:11:31 GMT", 
      "lat": 40.437850690867805, 
      "lon": -79.9909233197774, 
      "rt": "61A"
    }, 
    {
      "current_stop": {
        "stpid": "3241", 
        "stpnm": "Forbes Ave at Boyd St"
      }, 
      "destination": "Murray-Waterfront", 
      "dir": "OUTBOUND", 
      "distance": 2.9854166666666666, 
      "eta": "Sat, 17 Jan 2015 17:12:31 GMT", 
      "lat": 40.43851084104726, 
      "lon": -79.99453284035266, 
      "rt": "61D"
    }, 
    {
      "current_stop": {
        "stpid": "20691", 
        "stpnm": "5th Ave at Smithfield St"
      }, 
      "destination": "McKeesport", 
      "dir": "OUTBOUND", 
      "distance": 3.216666666666667, 
      "eta": "Sat, 17 Jan 2015 17:14:14 GMT", 
      "lat": 40.439916333333336, 
      "lon": -79.99838266666667, 
      "rt": "61C"
    }
  ], 
  "routes": {
    "61A": "OUTBOUND", 
    "61B": "OUTBOUND", 
    "61C": "OUTBOUND", 
    "61D": "OUTBOUND", 
    "67": "OUTBOUND", 
    "69": "OUTBOUND"
  }
}
```
