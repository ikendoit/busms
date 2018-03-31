BuSMS  -  Bus schedules, for your sms. 

FIRST: lets procrastinate: 
https://www.youtube.com/watch?v=2akbblhTfbM&t=9s

FORMAT :  STOP_ID (BUS_ID BUS_ID) 
STORY: 
    I was standing at the bus stop, wondering when the next bus would come. The stop didn't have the schedule board pinned on and it was frustrating .
   So I came home, tried to scrape translink's pdfs of bus schedules with python when I came across the wonderful Translink APIs.
   Then I remembered about Twilio, a phenomenal service which I encountered in a tech meetup I came mostly for free pizza.
   After 5 hours of hussling (mostly with ORM because Flask =)) ), I finally put up this service. I plan on using it a lot. 

TECH INFO: 
Hosted on a google cloud instance 
Python + Flask 
Redis caching
API: 
  Twilio : THE BEST sms service for developers: https://www.twilio.com/
  Translink: translink developer API: https://developer.translink.ca/

INSTALL: 
	pip3 install flask 
	pip3 install requests lxml json redis 
	apt-get install redis-* 
	
	then: python3 -m run flask 

	note: 
		you need a translink developer KEY, put it in modules/fetcher.py
		you need to put this on a production server, put the api /sms/ to twilio configuration in the "SMS service" section. 

MECHANISM: 
    The service when sees a new stop_id will fetch data from Translink API
    It will then store the data in redis, along with the current timestamp. For the next 5 minutes, if there is a new request, the service will use the pre-loaded data from redis. (This will leave less load on Translink as well as making Busms faster)
    There are some parsing, so that you can use bus ids after typing stop id. This will return data of specified buses.

FUTURE PLANS: 
    I have some python news scrapers that I will integrate in this service, so I can check my email, school mails, school notifications... (this is why I chose Python)
    I plan to play more with twilio, as their service are amazing and I don't have internet connection on my phone, so I rely a lot on sms. 

THANK YOU: 
  Translink for their wonderful developer api 
  Twilio for their great sms service, trial account (I'm poor) that last for more than 300 messages.
