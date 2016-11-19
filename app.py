#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    
    
    
    #baseurl = "https://query.yahooapis.com/v1/public/yql?"
    baseurl = "https://maps.googleapis.com/maps/api/geocode/json?"
    yql_query = makeYqlQuery(req)
    print(yql_query)
    if yql_query is None:
        return {}
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    print("YQL URL "+yql_url)
    loaded_json = json.load(urllib2.urlopen(yql_query))
    print("loaded Json "+loaded_json)
    result = urllib.urlopen(yql_query).read()
    print("result "+result)
    data = json.loads(result)
    print("data ")
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")
    if city is None:
        return None
    state = parameters.get("state")
    address = parameters.get("address")
    geo_base = "https://maps.googleapis.com/maps/api/geocode/json?address="
    geo_key = "&key=AIzaSyCYFoUBQrB9E1EDV7YI3EoNkBoHJRU7ww4"
    maprequest =  geo_base+address+", "+city+", "+state+geo_key
    print(maprequest)
    return maprequest

    #return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('results')
    print("query")
    print(query)
    print( 'query attempt '+['0'])
    if query is None:
        return {}

    result = query.get('geometry')
    print("result Makeweb " + result)
    if result is None:
        return {}

    channel = result.get('geometry')
    print("channel "+channel)
    if channel is None:
        return {}

    #item = channel.get('item')
    #location = channel.get('location')
    #units = channel.get('units')
    #if (location is None) or (item is None) or (units is None):
        #return {}

    #condition = item.get('condition')
    #if condition is None:
        #return {}

    # print(json.dumps(item, indent=4))

    #speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
     #        ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
    speech = channel
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
