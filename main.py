#!/usr/bin/env python

import json
import time
from gopigo import *

import paho.mqtt.client as mqtt


HOST = 'otis.leandog.com'
PORT = 52122
USERNAME = 'meetup'
PASSWORD = 'ze9mtHXHVYOp'

UID = 'dan.adiletta'
ONLINE_TOPIC = '/boat/meetup/{}/online'.format(UID)
STATUS_TOPIC = '/boat/meetup/{}/status'.format(UID)


class MqttService(object):

    def __init__(self):
        self._client = None

    def start(self):
        self._client = mqtt.Client(client_id=UID)
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

        # Set a will message stating that we are offline
        self._client.will_set(ONLINE_TOPIC, '0', retain=True)

        print('connecting to mqtt broker...')
        self._client.username_pw_set(USERNAME, PASSWORD)
        self._client.connect_async(HOST, PORT)

        # Paho needs a processing loop. loop_start will run this
        # in a different thread...
        self._client.loop_start()

        # ...but since we are running this from main, let's loop forever
        # on the main thread to keep the script running
        #self._client.loop_forever()


    def _on_disconnect(self, client, userdata, return_code):
        error = mqtt.error_string(return_code)
        print('disconnected from mqtt broker: {}'.format(error))

        # Reconnects using the client information provided previously.
        self._client.reconnect()

    def _on_connect(self, client, userdata, flags, return_code):
        print('connected to mqtt broker')

        # Publish a message stating that we are online
        self._client.publish(ONLINE_TOPIC, '1', retain=True)

        # Publish our device status
        epoch_time = int(time.time())
        message = '{} is sending messages from python!'.format(UID)
        payload = {'statusMessage': message, 'lastUpdated': epoch_time}
        payload_json = json.dumps(payload)
        self._client.publish(STATUS_TOPIC, payload_json, retain=True)

        # Subscribe to device statuses
        self._client.subscribe('/boat/meetup/#')

    def _on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode('utf-8')

        print('Got topic \"{}\" with payload \"{}\"'.format(topic, payload))


if __name__ == '__main__':
   mqtt_service = MqttService() 
   mqtt_service.start()

   while(True):
       distance = us_dist(15)
       time.sleep(2)
       self._client.publish("/boat/meetup/{}/distance".format(UID), str(distance))

