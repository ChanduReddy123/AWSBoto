import json
import boto3
client = boto3.client('logs')
#this is for getting the latest log stream from cloud watch and then getting logs from it
def lambda_handler(event, context):
    # getting the name of slatest log stream 
    logStreamName = client.describe_log_streams(
    logGroupName='/aws/lambda/describe',
    orderBy='LastEventTime',
    descending=True,
    limit=1
    )['logStreams'][0]['logStreamName']

    # getting the logs from latest log stream
    response = client.get_log_events(
    logGroupName='/aws/lambda/describe',
    logStreamName=logStreamName,
    limit=123,
    startFromHead=True
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
