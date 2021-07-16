import json
import urllib.parse
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        res = response['Body'].read()
        count = len(res.split())
        MY_SNS_TOPIC_ARN = 'SNS ARN GOES HERE'
        sns_client = boto3.client('sns')
        sns_client.publish(
        TopicArn = MY_SNS_TOPIC_ARN,
        Subject = 'Word Count Result',
        Message = 'The word count in the file ' + key + ' is ' + str(count)
        )
        response = Message
        return response
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e



