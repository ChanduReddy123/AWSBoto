import json
import boto3
import os
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#getting this event when we get a new object in the bucket 
def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket=event['Records'][0]['s3']['bucket']['name']
    key=event['Records'][0]['s3']['object']['key']
    #In lambda we can download files to /tmp directory and no other 
    destination='/tmp/'+key+'.eml'
    #downloding the object from s3 with key--name of object, bucket--name of bucket  to the path destinatio=/tmp/filename.eml
    s3.Bucket(bucket).download_file(key, destination)
    #using the attachments 
    ATTACHMENT = destination
    SENDER = "Feedback@blockit.co"
    AWS_REGION = "us-east-1"
    SUBJECT = "New support Email."
    BODY_HTML = """\
    <html>
    <head></head>
    <body>
    <h1>Hello!</h1>
    <h2>Please see the attached file for the new support mail.</h2>
    </body>
    </html>
    """
    CHARSET = "utf-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    #for person in list:
    msg = MIMEMultipart('mixed')
    #msg['Subject'] or ['From'] or ['To'] or ['CC'] should be of string types 
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = os.environ['TO']
    msg['CC'] = os.environ['CC']
    msg_body = MIMEMultipart('alternative')
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(htmlpart)
        
    att = MIMEApplication(open(ATTACHMENT, 'rb').read())
    att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))
    msg.attach(msg_body)
    msg.attach(att)
        #RECEPIENT=input
    try:
        response = client.send_raw_email(
        Source=SENDER,
        RawMessage={
                'Data':msg.as_string(),
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

