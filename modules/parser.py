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
    cur_min = datetime.datetime.now().minute
    cur_hour = datetime.datetime.now().hour
    interval = 5;
    do_scrape = False;
    old_data = r.get(stop_id)

    if old_data:
        old_min = old_data[0]
    else :
        old_min = cur_min

    #algorithm to check if a is within (b,b+interval), a & b = minutes
    if cur_min > old_min and cur_min <= old_min+interval: 
        do_scrape = False;
        print("We have this data "+stop_id);
    elif old_min >= 60-interval and cur_min <= 60 - interval: 
        cur_min+=60;
        if cur_min > old_min and cur_min <= old_min+interval: 
            do_scrape = False
            print("We have this data: "+stop_id);
        else:
            do_scrape = True
    else: 
        do_scrape = True

    #if data is still fresh
    #Current Setting: 10 minutes

    if not do_scrape:
        return old_data

    buses = []
    buses.append(cur_min);
    xml = fetch(stop_id);
    print("doing scraping");

    print(xml);
    data = etree.fromstring(xml);
    print(data)
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
