README

Enviroment requirement:
Python 3

required library:
shapely: https://pypi.org/project/shapely/

This is a basic version of monitoring and alert system. There are a lot of improvement can be done and features can be add. But I decide to keep it as now.

Based on requiremnet: "Anytime a phlebotomist goes out of the range your service should send an email to a specified email address", it should be an instant alert system. For example, it should send alert once it detect any phlebotomist is out of expected area instead of waiting 5 minutes to send the alert.

It uses threading as polling mechanism to query location API every X seconds, which is configurable to make the good balance between not overloading the API and the accuracy of the warning. Here I query the API every 5 seconds and set the alert cooldown to 5 minutes in order to avoid duplicated spammy alert for same phlebotomist.

There are also some print statement which can be converted to server logging for potential debugging purpose

How to run the monitoring and alert sever:

put phlebotomistLocationMonitoringAlert.py on monitoring server (or any server that keeps running), then run `python3 sprinterTest.py` and keep it running

As long as it is running, it will check all phlebotomists' location every 5 seconds. If any phlebotomist is out of expected area, it will instantly send alert email to EMAIL_ALERT_RECIEVER_ADDRESS. Also there is a cooldown mechanism that, if the system has send alert email for certain phlebotomist, it will wait 5 minutes before sending another alert email for the same phlebotomist.

