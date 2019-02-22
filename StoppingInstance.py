import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('ec2')
    search=[
        {
            'Name': 'tag:Owner',
            'Values': ['chandrashekar.bekkem','chandu']
        },
    ]
    response = client.describe_instances(Filters=search)
    value=[]
    for limit in response['Reservations']:
        value.append(limit['Instances'][0]['InstanceId'])
    response=client.stop_instances(InstanceIds=value)

    return response
