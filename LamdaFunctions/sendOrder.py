import json
import boto3

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    sns = boto3.client('sns')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/831294309591/taxi-queue'  # Replace with the actual URL of the HalifaxTaxi queue
    sns_topic_arn = 'arn:aws:sns:us-east-1:831294309591:HalifaxTaxiOrder'  # Replace with the actual ARN of your SNS topic

    # Receive multiple messages from the queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    )

    # Check if there are available messages
    if 'Messages' in response:
        messages = response['Messages']
        order_details = []

        for message in messages:
            order = json.loads(message['Body'])
            order_details.append(format_order(order))

        # Create a formatted message body with multiple orders
        message_body = '\n\n'.join(order_details)

        # Trigger SNS to send details to your topic
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject='New Order',
            Message=message_body
        )

        # Delete the messages from the queue
        entries = [{'Id': message['MessageId'], 'ReceiptHandle': message['ReceiptHandle']} for message in messages]
        sqs.delete_message_batch(
            QueueUrl=queue_url,
            Entries=entries
        )

        return {
            'statusCode': 200,
            'body': 'Order details sent to your SNS topic'
        }

    return {
        'statusCode': 200,
        'body': 'No orders in the queue'
    }

def format_order(order):
    car_type = order['car_type']
    car_accessories = ', '.join(order['car_accessories'])
    street_address = order['street_address']

    return f'Order Details:\n\nCar Type: {car_type}\nCar Accessories: {car_accessories}\nStreet Address: {street_address}'