from twilio.rest import Client
from os import environ


def send_text(msg, to_cid):
    twilio = Client(environ["TWILIO_SID"], environ["TWILIO_TOKEN"])
    twilio.messages.create(body=msg, from_='+14702646307', to=to_cid)
