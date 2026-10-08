# Insert this script on Lambda -> Code -> Deploy
# Then test with JSON from step 26 on documentation.md

import boto3

cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

TOPIC_ARN = arn:aws:sns:us-east-2:874841217397:PiAlerts:902530d1-07ce-4892-9e07-9667ce975591

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
