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

# Step 11 - Create a Lambda Function
Search AWS:
Lambda

Click:
Create Function

Choose:
Author from scratch

Function Name:
PiMetricsToCloudWatch

Runtime:
Python 3.13

Click:
Create Function

# Step 12 - Give Lambda Permission to Write CloudWatch
Open:
Configuration -> Permissions

Click:
Lambda execution role

Click:
Add permissions -> attach policies

Search and attach:
CloudWatchFullAccess

# Step 13 - Add Lambda Core
Replace the default Lambda code with:
Lambda -> Functions -> PiMetricsToCloudWatch

import json
import boto3
 
cloudwatch = boto3.client('cloudwatch')
 
def lambda_handler(event, context):
 
cloudwatch.put_metric_data(
Namespace='PiMonitor',
MetricData=[
{
'MetricName': 'CPUUsage',
'Value': float(event['cpu']),
'Unit': 'Percent'
},
{
'MetricName': 'MemoryUsage',
'Value': float(event['memory']),
'Unit': 'Percent'
},
{
'MetricName': 'DiskUsage',
'Value': float(event['disk']),
'Unit': 'Percent'
}
]
)
 
return {
'statusCode': 200
}

Then click:
Deploy

You should see:
Successfully updated function

Test Lambda:
Click Test

Use this JSON:
{
  "cpu": 25,
  "memory": 40,
  "disk": 15
}

Save it and click:
Test

Results:
statusCode 200

# Step 15 - Connect AWS IoT Rule to Lambda
AWS IoT Core -> Message Routing -> Rules

Add Another Action:
Actions -> Add Action -> Lambda -> Choose your function you created

# Step 16 - Start Sending Telemetry
On your Pi:
source venv/bin/activate
cd ~/projects/aws-iot-monitor
python3 monitor.py

# Step 17 - Verify Lambda Executions
Lambda -> PiMetricsToCloudWatch -> Monitor
Check for -> Invovations

# Step 18 - Verify CloudWatch Metrics
Navigate:
CloudWatch -> Metrics

Click:
All metrics

Then:
Custom Namespaces

You should see:
PiMonitor

Click it and you should see:
CPUUsage
MemoryUsage
DiskUsage

# Step 19 - Create a Dashboard
Navigate:
CloudWatch -> Dashboards -> Create dashboards

Name:
PiMonitorDashboards

Widget 1:
Add - Line Graph
Select - CPUUsage
Title - Raspberry Pi CPU Utilization

Widget 2:
Add - Line Graph
Plain Text - MemoryUsage
Title - Raspberry Pi Memory Utilization

Widget 3:
Add - Line Graph
Select - DiskUsage
Title - Raspberry Pi Disk Utilization

# Step 20 - Create SNS Topic
Search:
SNS

Open:
Simple Notification Service

Navigate:
Topics -> Create Topic

Choose:
Standard

Name:
PiAlerts

Click:
Create Topic

# Step 21 - Create Email Subscription
Inside:
PiAlerts

Click:
Create Subscription

Protocol: 
Email

Endpoint:
your_email@example.com

Click:
Create Subscription

# Step 22 - Confirm Subscription
Check your email

# Step 23 - Copy the SNS Topic ARN
Inside:
PiAlerts

Copy:
Topic ARN
arn:aws:sns:us-east-2:874841217397:PiAlerts:902530d1-07ce-4892-9e07-9667ce975591

# Step 24 - Update Lambda Function
Lambda -> PiMetricsToCloudWatch

Replace cold with:
import boto3

cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

TOPIC_ARN = "arn:aws:sns:us-east-2:874841217397:PiAlerts"

def lambda_handler(event, context):

    cpu = float(event['cpu'])
    memory = float(event['memory'])
    disk = float(event['disk'])

    cloudwatch.put_metric_data(
        Namespace='PiMonitor',
        MetricData=[
            {
                'MetricName': 'CPUUsage',
                'Value': cpu,
                'Unit': 'Percent'
            },
            {
                'MetricName': 'MemoryUsage',
                'Value': memory,
                'Unit': 'Percent'
            },
            {
                'MetricName': 'DiskUsage',
                'Value': disk,
                'Unit': 'Percent'
            }
        ]
    )

    if cpu > 80:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Raspberry Pi CPU Alert",
            Message=f"CPU usage exceeded threshold: {cpu}%"
        )

    return {
        'statusCode': 200
    }

Click:
Deploy

# Step 25 - Grant Lambda Permission to Send SNS
Go to:
Lambda -> Configuration -> Permissions

Open the execution role.

Attach & save:
AmazonSNSFullAccess

# Step 26 - Test the Alert
Inside Lambda:
Test

Use JSON to execute the test:
{
"cpu": 95,
"memory": 30,
"disk": 20
}

# Step 27 - SNS Alert
You will now receive an SNS alert either by email or phone based on preference.



    


