"""
    Date: May 2019
    Dscription: Example MQTT python client program to connect to a Raspberry Pi running a Mosquitto
    mqtt broker and ChirpStack LoRaWAN Gateway Server. This code subscribes to an application stream publishing lora data from a lora-E5 mini end device.
    Note: Change the ip address to match the Pi being used.
"""
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    pl_socket = '{"contact": ""}'
    print("Connected with result code "+str(rc))
    # client.subscribe("application/2/device/2cf7f12024900aea/rx")
    client.subscribe("application/2/#")
    client.publish("application/2/device/2cf7f12024900aea/tx", ' { "confirmed": true, "fPort": 8, "data":  bytes([0x01, 0x02, 0x03]) }') 
    # client.publish("application/2/device/2cf7f12024900aea/command/down", ' { "confirmed": true, "fPort": 8, "data": "test reply----" }')
    # application/2/device/2cf7f12024900aea/command/down
    

def on_message(client, userdata, msg):
    #print("Payload type:" + type(msg.payload))
    result = msg.payload.decode("utf-8")
    print(time.asctime())
    print(msg.topic + " " + msg.payload.decode("utf-8"))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.7", 1883, 60)
print(time.asctime())
client.loop_forever()
