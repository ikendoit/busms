import json 
import datetime
import redis
import lxml.etree as etree
from modules.fetcher import fetch

r = redis.StrictRedis(host="localhost",port=6379, db=0)

# run program, return json data, store it in redis
# @params: stop_d 
# @return: dict object
def parse(stop_id): 
    #set time stamp: hour*60+minute; compare with old timestamp to 
    #see if data is still fresh
    cur_min = datetime.datetime.now().minute
    cur_hour = datetime.datetime.now().hour
    cur_time = cur_hour*60 + cur_min

    interval = 5;
    do_scrape = False;
    old_data = r.get(stop_id)

    if old_data:
        old_time = old_data[0]
    else :
        old_time = cur_time

    #check if current time stamp is new or old
    if cur_time > old_time and cur_time <= old_time+interval: 
        do_scrape = False;
        print("We have this data "+stop_id);
    else: 
        print("init fetching process for"+stop_id);
        do_scrape = True

    #if data is still fresh
    #Current Setting: 10 minutes

    if not do_scrape:
        return old_data

    buses = []
    buses.append(cur_time);
    xml = fetch(stop_id);

    data = etree.fromstring(xml);
    for bus_data in data.iterchildren("*"): 
        bus = {}
        bus["schedules"] = []
        for ele in bus_data.iterchildren("*"):
            if ele.tag == "RouteNo":
                bus["name"] = ele.text;
            if ele.tag == "Schedules": 
                for sched in ele.iterchildren("*"):
                    sched_data = {};

                    for sched_ele in sched.iter("ExpectedLeaveTime"):
                        sched_data["time"] = sched_ele.text;

                    for sched_ele in sched.iter("CancelledTrip"):
                        sched_data["tripcancel"] = sched_ele.text;

                    for sched_ele in sched.iter("CancelledStop"):
                        sched_data["stopcancel"] = sched_ele.text;

                    bus["schedules"].append(sched_data);
        buses.append(bus);

    r.set(stop_id, buses)

    return buses
