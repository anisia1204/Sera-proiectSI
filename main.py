from flask import Flask
from flask_restful import Api, Resource, reqparse
from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO
import adafruit_dht
from board import *
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import Adafruit_DHT

import numpy as np

GPIO.setmode(GPIO.BCM)

# pompa - relay in1
GPIO.setup(27,GPIO.OUT)

# fan - relay in2
GPIO.setup(22,GPIO.OUT)

#air temperature and humidity
SENSOR_PIN = Adafruit_DHT.DHT11 #D21
GPIO_temp = 21
humidity, temperature = Adafruit_DHT.read_retry(SENSOR_PIN,GPIO_temp)

#light sensor
GPIO.setup(20, GPIO.IN)

GPIO_umid_sol = 26
GPIO.setup(GPIO_umid_sol, GPIO.IN)

app = Flask(__name__)
api = Api(app)

class DataBase(Resource):
     def get(self,id = 0):
      print('\"sensor\": [\n{')
      if id == 0:
        return "Request invalid", 404
      #light sensor
      if id == 1:
        if GPIO.input(20):
           message = "It's dark!"
        else:
           message = "It's light!"
        dictionary = {
           "sensors": {
              "sensor": "light",
              "value": GPIO.input(20) # 1 - dark, 0 - light
           }
        }
        return dictionary
      
      # humidity soil
      if id == 2:
        if GPIO.input(GPIO_umid_sol):
           message = "Water detected"
        else:
           message = "No water detected"
        dictionary = {
           "sensors": {
              "sensor": "moisture",
              "value": GPIO.input(GPIO_umid_sol) 
           }
        }
        return dictionary
      
      # air humidity
      if id == 3:
        dictionary = {
           "sensors": {
              "sensor": "humidity - air",
              "value": humidity
           }
        }
        return dictionary, 200
      
      # air temperature
      if id == 4:
        dictionary = {
           "sensors": {
              "sensor": "temperature - air",
              "value": temperature
           }
        }
        return dictionary, 200
      
      # pump
      if id == 5:
         GPIO.output(27, True)
         print("pump open")
         time.sleep(10)
         GPIO.output(27, False)
         return "the plants were watered"
      
      # fan
      if id == 6:
         GPIO.output(22, True)
         print("fan open")
         time.sleep(10)
         GPIO.output(22, False)
         return "the plants were vantilated"
      
      return "Not found", 404
     
api.add.resource(DataBase, "/api", "/api/<int:id>")

if __name__ == '__main__':
   app.run(debug = True, host = '0.0.0.0')
                     