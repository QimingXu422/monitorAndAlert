import requests
import threading
import json
import smtplib
import time
from email.message import EmailMessage
from shapely.geometry import mapping, shape
from enum import Enum

#configuration:
# Please use this part to configure the email sender, reciever and how often the system should check phlebotomist' location
# Use App Password to meet gmail privacy requirement
EMAIL_ALERT_SENDER_ADDRESS = "sprinterwarning@gmail.com"
EMAIL_ALERT_SENDER_APP_PASSWORD = "frjkplnbmuifdqbt"
EMAIL_ALERT_TEST_RECIEVER_ADDRESS = "sprinterwarning@yahoo.com"
EMAIL_ALERT_RECIEVER_ADDRESS = "coding-challenges+alerts@sprinterhealth.com"
# the check interval can be changed to meet the bussiness need and find a balance between server load and accuracy, 
# here I use 5 sec as default
CHECK_INTERVAL = 5.0 
# the alert cooldown means how long should the system wait before sending duplicated warning for same phlebotomist
# this is to avoid overwhelming alert email
ALERT_COOLDOWN = 300.0

class AlertType(Enum):
    MISSING = "missing"
    OUT = "out"

alert_cooldown_dict = {}

def send_email(phlebotomist_id, error_type, alert_cooldown_dict):

	current_timestamp = time.time()
	
	if alert_cooldown_dict.get(phlebotomist_id) == None or current_timestamp - alert_cooldown_dict.get(phlebotomist_id) >= ALERT_COOLDOWN:
		print('sending alert message for', phlebotomist_id)
		# it currently just suppot two cases: 
		# 1. cannot get location of phlebotomist and 2. phlebotomist is out of expected area, 
		# If needed we can expand this part to support more alert cases
		error_message = "[Qiming Xu] Phlebotomist #%i is out of expected zone" % phlebotomist_id if error_type == AlertType.OUT else "[Qiming Xu] Cannot get location of Phlebotomist #%i" % phlebotomist_id 

		# create email
		msg = EmailMessage()
		msg['Subject'] = error_message
		msg['From'] = EMAIL_ALERT_SENDER_ADDRESS
		msg['To'] = EMAIL_ALERT_RECIEVER_ADDRESS
		msg.set_content(error_message)

		# send email
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		    smtp.login(EMAIL_ALERT_SENDER_ADDRESS, EMAIL_ALERT_SENDER_APP_PASSWORD)
		    smtp.send_message(msg) 
		print('sent alert message for', phlebotomist_id)
		alert_cooldown_dict[phlebotomist_id] = current_timestamp

def validate_location(phlebotomist_id, alert_cooldown_dict):

	url = 'https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/%i' % phlebotomist_id
	response = requests.get(url)

	if response.status_code != 200:
		send_email(phlebotomist_id, AlertType.MISSING, alert_cooldown_dict)

	response_json = response.json()

	# send alert email if cannot get position infomation from response
	try:
		phlebotomist_location = response_json['features'][0]['geometry']
	except KeyError:
		send_email(phlebotomist_id, AlertType.MISSING, alert_cooldown_dict)
		return
	try: 
		expected_area = response_json['features'][1]['geometry']
	except KeyError:
		send_email(phlebotomist_id, AlertType.MISSING, alert_cooldown_dict)
		return
	phlebotomist_location_point = shape(phlebotomist_location)
	expected_area_polygon = shape(expected_area)

	# use shapely library to determine if phlebotomist is in expeceted area or eactly on the boundary
	if not phlebotomist_location_point.within(expected_area_polygon) and not expected_area_polygon.touches(phlebotomist_location_point):
		send_email(phlebotomist_id, AlertType.OUT, alert_cooldown_dict)

def start_monitoring():
	threading.Timer(CHECK_INTERVAL, start_monitoring).start()
	# check phlebotomist from id 1 to 6
	for phlebotomist_id in range(1, 7):
		validate_location(phlebotomist_id, alert_cooldown_dict)

start_monitoring()



