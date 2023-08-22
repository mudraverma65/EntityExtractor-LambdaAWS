import json
import boto3

def lambda_handler(event, context):
    # Retrieve the bucket and file information from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Extract the entity name from the file key
    entity_name = file_key.split('.')[0]

    # Retrieve the named entity data from the JSON file
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=file_key)
    named_entities = json.loads(response['Body'].read().decode('utf-8'))

    # Update the DynamoDB table with the named entity data
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('b00932103-a3')

    # Check if there are named entities to update
    if not named_entities:
        print('No named entities found in the file')
        return {
            'statusCode': 400,
            'body': 'No named entities found in the file'
        }

    with table.batch_writer() as batch:
        for entity, value in named_entities.items():
            batch.put_item(Item={
                'key': entity,
                'value': value
            })

    print('DynamoDB table updated successfully')
    return {
        'statusCode': 200,
        'body': 'DynamoDB table updated successfully'
    }
