# Built an AWS IoT monitoring solution using Raspberry Pi 5, Python, MQTT, and AWS IoT Core. 
# Implemented certificate-based device authentication and published real-time system telemetry including CPU, memory, and disk utilization to AWS.

import json
import time
from awscrt import mqtt
from awsiot import mqtt_connection_builder

ENDPOINT = "a35gz04f3vvddk-ats.iot.us-east-2.amazonaws.com"

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath="certs/certificate.pem.crt",
    pri_key_filepath="certs/private.pem.key",
    ca_filepath="certs/AmazonRootCA1.pem",
    client_id="raspberrypi5",
    clean_session=False,
    keep_alive_secs=30
)

print("Connecting to AWS IoT...")

mqtt_connection.connect().result()

print("Connected!")

message = {
    "device": "raspberrypi5",
    "status": "hello from raspberry pi"
}

mqtt_connection.publish(
    topic="pi/metrics",
    payload=json.dumps(message),
    qos=mqtt.QoS.AT_LEAST_ONCE
)

print("Message sent!")
