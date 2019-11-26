## BuSMS - Bus schedules, for your sms.

FIRST: lets procrastinate: 

https://www.youtube.com/watch?v=2akbblhTfbM&t=9s

FORMAT :  STOP_ID (BUS_ID BUS_ID) 

### Story: 

   - I was standing at the bus stop, wondering when the next bus would come. The stop didn't have the schedule board pinned on and it was frustrating .

   - So I came home, tried to scrape translink's pdfs of bus schedules with python when I came across the wonderful Translink APIs.

   - Then I remembered about Twilio, a phenomenal service which I encountered in a tech meetup I came mostly for free pizza.

   - After 5 hours of hussling (mostly with ORM because Flask =)) ), I finally put up this service. I plan on using it a lot. 

### TECH INFO
* Hosted on a Google Cloud Instance
* Python + [Flask](https://www.fullstackpython.com/flask.html) 
* Redis caching
* Twilio API: THE BEST sms service for developers: https://www.twilio.com/
* Translink: Translink developer API: https://developer.translink.ca/

### Requirements

* Retrieve Translink Developer Key [here](https://developer.translink.ca/) and put it in `modules/fetcher.py'
* Setup your own Twilio account and set SMS webhook to `/sms` endpoint in your Twilio console
* Note: Your API must be public 

### How to run
```
// installing dependencies
pip3 install flask 
pip3 install requests lxml json redis 
apt-get install redis-* 

// running
python3 -m run flask 
```


### Usage

* The service when sees a new stop_id will fetch data from Translink API

* It will then store the data in redis, along with the current timestamp. For the next 5 minutes, if there is a new request, the service will use the pre-loaded data from redis. (This will leave less load on Translink as well as making Busms faster)

* There are some parsing, so that you can use bus ids after typing stop id. This will return data of specified buses.

### Future plans

* I have some python news scrapers that I will integrate in this service, so I can check my email, school mails, school notifications... (this is why I chose Python)

* I plan to play more with twilio, as their service are amazing and I don't have internet connection on my phone, so I rely a lot on sms. 

THANK YOU: 

  - Translink for their wonderful developer api 

  - Twilio for their great sms service, trial account (I'm poor) that last for more than 300 messages.
