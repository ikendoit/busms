import requests 

def fetch(stop_id):
    data = requests.get("http://api.translink.ca/rttiapi/v1/stops/"+stop_id+"/estimates?apikey=MMKpRVbHI434lbDjTwZi");

    return data.text

