import paho.mqtt.client as mqtt
import json
import base64
import time

dev_eui = bytes([0x2C,0xF7,0xF1,0x20,0x24,0x90,0x0A,0xEA])

def on_connect(client,userdata,flags,rc):
    print("Connected with result code:"+str(rc))
    client.subscribe("application/+/device/+/error")
    datatosend = b'\x01\x02\x04\x00\x00\x00\x00'
    datatosendb64 = base64.b64encode(datatosend)
    packettosend = {
        "confirmed": True,
        "fPort": 3,
        "data": "aGFsbG8=" # str(datatosendb64)
    }
    json_packettosend = json.dumps(packettosend)
    client.publish("application/2/device/2cf7f12024900aea/tx", json_packettosend, 0, False)

def on_message(client, userdata, msg):
    #print("Payload type:" + type(msg.payload))
    result = msg.payload.decode("utf-8")
    print(time.asctime())
    print(msg.topic + " " + msg.payload.decode("utf-8"))

mqttc= mqtt.Client()
mqttc.on_connect=on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.0.7",1883,60)
mqttc.loop_forever()
