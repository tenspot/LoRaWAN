"""
Date: July 2021

Using the ChirpStack API to enqueue downlink data to tx to an end node (LoRa-E5 mini in this case.)

Source: https://www.chirpstack.io/application-server/api/python-examples/

Need to set the IP address of the LoRaWAN Gateway server and an api_token from the ChirpStack gateway
web interface.



"""

import os
import sys
import json
import base64


from chirpstack_api.as_pb.external import api
import grpc

# Configuration.

# This must point to the API interface.
server = "192.168.0.7:8080"

# The DevEUI for which you want to enqueue the downlink.
# 2C:F7:F1:20:24:90:0A:EA
dev_eui = bytes([0x2C,0xF7,0xF1,0x20,0x24,0x90,0x0A,0xEA])

# The API token (retrieved using the ChirpStack web-interface).
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiZWQ5YjA1MWMtOGJlNS00NzE1LWJhNmQtOGNjNzdhNDAxMjI4IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTYyNzQwMjM4Niwic3ViIjoiYXBpX2tleSJ9.XnLezifiSNbIxLeNdv9NrVkR4UCD-sOHlU3DoW1QLzU"

if __name__ == "__main__":
  # Connect without using TLS.
  channel = grpc.insecure_channel(server)

  # Device-queue API client.
  client = api.DeviceQueueServiceStub(channel)

  # Define the API key meta-data.
  auth_token = [("authorization", "Bearer %s" % api_token)]

  # Construct request.
  datatosend = bytes("This is a test string from VSCode.", 
'utf-8')
  datatosendb64 = base64.b64encode(datatosend).decode("utf-8")
  # Example 1 - raw base64 string
  # packettosend = {
      # "confirmed": True,
      # "fPort": 3,
      # "data": "aGFsbG8=",
  # }

  # packettosend = {
    # "confirmed": True,
    # "fPort": 3,
    # "data": str(datatosendb64)
  # }

  packettosend = {
    "confirmed": True,
    "fPort": 3,
    "data": "THIS"
  }
# 
  # json_packettosend = bytes(json.dumps(packettosend), "utf-8")
  json_packettosend = bytes(str(packettosend),"utf-8")
  req = api.EnqueueDeviceQueueItemRequest()
  req.device_queue_item.confirmed = False
  # Example A - send some bytes
  # req.device_queue_item.data = bytes([0x01, 0x02, 0x03])
  # Example B - send a byte encoded string
  req.device_queue_item.data = datatosend
  # Example C - send a JSON encoded package
  # req.device_queue_item.data = json_packettosend
  req.device_queue_item.dev_eui = dev_eui.hex()
  req.device_queue_item.f_port = 10

  resp = client.Enqueue(req, metadata=auth_token)

  # Print the downlink frame-counter value.
  print(resp.f_cnt)