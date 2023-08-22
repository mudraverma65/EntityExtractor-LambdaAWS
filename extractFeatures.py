import json
import boto3
import re

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Retrieve the bucket and file information from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Retrieve the file content
    response = s3.get_object(Bucket=bucket, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')

    # Use regex to extract named entities
    named_entities = {}

    matches = re.findall(r'\b[A-Z][a-zA-Z]+\b(?![a-z])', file_content)
    for match in matches:
        named_entities[match] = 1

    # Save the JSON array as a file in a new S3 bucket only if named entities are found
    tags_bucket = 'tags-b00932103'  
    new_file_key = file_key.replace('.txt', 'ne.txt')  # Modify the file key to add 'ne' suffix
    
    if named_entities:
        s3.put_object(Body=json.dumps(named_entities), Bucket=tags_bucket, Key=new_file_key)
    else:
        print('No named entities found in the file')

    return {
        'statusCode': 200,
        'body': json.dumps('Named entities extracted and saved successfully')
    }
