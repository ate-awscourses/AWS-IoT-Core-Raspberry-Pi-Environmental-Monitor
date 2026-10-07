# Step 1 - Create AWS IoT Thing
AWS Console:
AWS IoT Core -> Manage -> All Devices -> Things -> Create Thing

Choose:
Single Thing

Name:
raspberrypi5-monitor

# Step 2 - Generate Device Certificates
Choose:
Auto-generate certificate

Download:
certificate.pem.crt
private.pem.key
public.pem.key
AmazonRootCA1.pem

Create a folder on the Pi and add the downloaded certs there:
mkdir -p ~/aws-iot/certs

# Step 3 - Create IoT Policy
Create policy: 
{
"Version":"2012-10-17",
"Statement":[
{
"Effect":"Allow",
"Action":[
"iot:Connect",
"iot:Publish",
"iot:Subscribe",
"iot:Receive"
],
"Resource":"*"
}
]
}

Attach:
Policy -> Certificate -> Thing

# Step 4 - Finding IoT Endpoint
AWS IoT Core: 
Settings -> copy your Endpoint and save it

# Step 5 - Install Software on Raspberry PI (Shell)
Update System:
sudo apt update
sudo apt upgrade -y

Install Python tools:
sudo apt install python3-pip -y

Install MQTT SDK:
pip3 install awsiotsdk

Install metrics package:
pip3 install psutil

# Step 6 - Create Python Publisher
Create: 
nano monitor.py

import json
import psutil
import time
from awscrt import mqtt
from awsiot import mqtt_connection_builder
 
ENDPOINT = "YOUR-ENDPOINT"
 
mqtt_connection = mqtt_connection_builder.mtls_from_path(
endpoint=ENDPOINT,
cert_filepath="certs/certificate.pem.crt",
pri_key_filepath="certs/private.pem.key",
ca_filepath="certs/AmazonRootCA1.pem",
client_id="raspberrypi5",
clean_session=False,
keep_alive_secs=30
)
 
mqtt_connection.connect().result()
 
while True:
payload = {
"cpu": psutil.cpu_percent(),
"memory": psutil.virtual_memory().percent,
"disk": psutil.disk_usage("/").percent
}
 
mqtt_connection.publish(
topic="home/pi/metrics",
payload=json.dumps(payload),
qos=mqtt.QoS.AT_LEAST_ONCE
)
 
print(payload)
 
time.sleep(30)

Run on shell:
python3 monitor.py

# Step 7 - Test the MQTT Messages
AWS Console:
IoT Core -> MQTT Test client

Subscribe:
home/pi/metrics

You should see:
Your metrics that you ran earlier from your Pi

# Step 8 - Store Data in DynamoDB
Create table:
PiMetrics

Partition Key:
deviceId

Sort Key:
timestamp

# Step 9 - Create IoT Rule
AWS Iot Core:
Message Routing -> Rules

SQL:
SELECT *
FROM 'home/pi/metrics'

Action:
Insert into DynamoDB

# Step 10 - Add CloudWatch Monitoring
Create another rule (Message Routing -> Rules)
SELECT cpu
FROM 'home/pi/metrics'

Send data to:
CloudWatch

# Step 11 - Add SNS Alerts
Create SNS Topic
pi-alerts
Subscribe your email

Lambda logic:
IF CPU > 50%
Send Email Alert
