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

**Test plan**

Change ```EMAIL_ALERT_RECIEVER_ADDRESS``` to ```EMAIL_ALERT_TEST_RECIEVER_ADDRESS``` at line 45.
run ```python3 phlebotomistLocationMonitoringAlert.py``` for a while

check test email and see alerts are recieved:
<img width="890" alt="Screenshot 2022-12-30 at 9 10 55 PM" src="https://user-images.githubusercontent.com/30333198/210125723-dbd71b38-b536-4d0f-a731-ec954f57c473.png">
<img width="920" alt="Screenshot 2022-12-30 at 9 11 26 PM" src="https://user-images.githubusercontent.com/30333198/210125739-f0e6b8a5-1bf0-40f5-9858-2d0467bbe737.png">
<img width="910" alt="Screenshot 2022-12-30 at 9 11 42 PM" src="https://user-images.githubusercontent.com/30333198/210125743-77ce3a68-8308-4b58-9efd-27fba0ec1033.png">
