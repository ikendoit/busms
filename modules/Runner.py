from modules.fetcher import fetch
from modules.parser import parse
import json

#if this is a bytes type (when pulling data out of redis)
#then convert it to a python object (dict or list)
def decode_api(all_data):
    if not isinstance(all_data, list) and not isinstance(all_data,dict):
       all_data = all_data.decode("utf-8");
       all_data = all_data.replace('"',"!!")
       all_data = all_data.replace("'",'"')
       all_data = all_data.replace("!!","'")
       all_data = json.loads(all_data)

    return all_data

#return string result for bus schedules
#param: message: query data: {Stop_ID BUS_ID BUS_ID ..} or {Stop_ID}
#return: string response: {bus}:({schedules}), ..
def runner(message):
    message = message.split(" ");
    stop_id = message[0]
    all_data = parse(stop_id)
    all_data = decode_api(all_data)

    response = ""

    for data in all_data:
        if not isinstance(data,int) and "schedules" in data: 
            if (len(message) > 1 and data["name"] in message) or len(message)==1:
                response = response+data["name"]+":(";
                for sched in data["schedules"]: 
                    if sched["tripcancel"] == "false" and sched["stopcancel"]=="false": 
                        if len(sched["time"]) > 11: 
                            sched["time"] = sched["time"][:-10]
                        response = response+sched["time"]+","
                response = response+") "
    print(len(response))
    return response

#return data result for bus schedules
#param: message: query data: {Stop_ID BUS_ID BUS_ID ..} or {Stop_ID}
#return: json repsonse: 
#   [timestamp:int, { "name": "bus", "schedules": 
#                    [{ 
#                        "stopcancel": "true"//"false"
#                        "tripcancel": "true"//"false"
#                        "time": string(time of bus)
#                    }]
#                   }, .. 
#   ]
def runner_api(message):
    message = message.split(" ");
    stop_id = message[0]
    all_data = parse(stop_id)
    all_data = decode_api(all_data)

    return all_data;


if __name__=="__main__":
    runner("50077")
