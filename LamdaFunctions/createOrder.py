import random
import json
import boto3

CAR = ['Compact', 'Mid-size Sedan', 'SUV', 'Luxury', 'Convertible', 'Pickup Truck']
ADDON = ['GPS', 'Camera', 'Bluetooth', 'Wi-Fi', 'Child Seat']
CLIENT = ['6050 University Avenue', '123 Main Street', '789 Elm Road', '456 Pine Lane', '321 Oak Avenue']

def lambda_handler(event, context):
    sns = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:831294309591:HalifaxNewOrder' 

    car_type = random.choice(CAR)
    car_accessories = random.sample(ADDON, k=random.randint(0, len(ADDON)))
    street_address = random.choice(CLIENT)

    message = {
        'car_type': car_type,
        'car_accessories': car_accessories,
        'street_address': street_address
    }

    sns.publish(
        TopicArn=sns_topic_arn,
        Subject='New Order',
        Message=json.dumps(message)
    )

    return {
        'statusCode': 200,
        'body': 'Message sent to SNS topic successfully'
    }
