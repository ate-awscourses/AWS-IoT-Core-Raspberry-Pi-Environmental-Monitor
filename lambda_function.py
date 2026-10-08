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