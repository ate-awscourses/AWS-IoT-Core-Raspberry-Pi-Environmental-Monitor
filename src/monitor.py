import json
import time
import psutil
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

while True:
    payload = {
        "device": "raspberrypi5",
	"timestamp": str(int(time.time())),
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent
    }

    mqtt_connection.publish(
        topic="pi/metrics",
        payload=json.dumps(payload),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    print(payload)

    time.sleep(30)
 
