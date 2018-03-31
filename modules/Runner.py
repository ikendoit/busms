from modules.fetcher import fetch
from modules.parser import parse
import json

def runner(message):

    message = message.split(" ");
    stop_id = message[0]

    all_data = parse(stop_id)

    #if this is a bytes type (when pulling data out of redis)
    if not isinstance(all_data, list):
        all_data = all_data.decode("utf-8");
        all_data = all_data.replace('"',"!!")
        all_data = all_data.replace("'",'"')
        all_data = all_data.replace("!!","'")

        all_data = json.loads(all_data)

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


if __name__=="__main__":
    runner("50077")
