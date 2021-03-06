#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class Lichtsteuerung2(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()
        
    # --> Sub callback function, one per intent
    def LichtAus2_callback(self, hermes, intent_message):
        # close the session first by sending an empty string
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        house_room = intent_message.slots.Wohnraum.first().value # We extract the value from the slot "Wohnraum"
        light_cmd = intent_message.slots.LightCmd.first().value # We extract the value from the slot "LightCmd"
        result_sentence = "Licht {}".format(str(light_cmd))
        result_sentence = result_sentence + (" : {}".format(str(house_room)))
        
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, result_sentence, "")

    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def Lichtsteuerung2_master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'karlu:LichtAus2':
            self.LichtAus2_callback(hermes, intent_message)
#        if coming_intent == 'intent_2':
 #           self.intent_2_callback(hermes, intent_message)
        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.Lichtsteuerung2_master_intent_callback).start()

if __name__ == "__main__":
    Lichtsteuerung2()
