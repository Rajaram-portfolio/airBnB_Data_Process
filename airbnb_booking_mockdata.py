import json
import random
import boto3
import datetime

sqs_client = boto3.client('sqs')
sqs_queue = 'https://sqs.us-west-1.amazonaws.com/709114567321/AirbnbBookingQueue'

def generate_airbnb_booking(num):
    booking_data=[]
    for _ in range(num):
        bookingId = "B"+str(random.randint(1, 99))
        userId = "U"+str(random.randint(10, 200))
        propertyId = random.randint(1000, 9999)
        location = random.choice(["New York, USA", "London, UK", "Paris, France", "Tokyo, Japan", "Sydney, Australia"])
        startDate = datetime.datetime.now() + datetime.timedelta(days=random.randint(0,4))
        endDate = datetime.datetime.now() + datetime.timedelta(days=random.randint(4,8))
        price = round(random.uniform(10, 50), 2)
        
        data={
        "bookingId" : bookingId,
        "userId" : userId,
        "propertyId" : propertyId,
        "location" : location,
        "startDate" : startDate.strftime('%Y-%m-%d'),
        "endDate" : endDate.strftime('%Y-%m-%d'),
        "price" : price

         }
        booking_data.append(data)
        
        sqs_client.send_message(QueueUrl=sqs_queue, MessageBody=json.dumps(booking_data))

    print(booking_data)
    
def lambda_handler(event, context):
    # TODO implement
    generate_airbnb_booking(3)
    #sqs_client.send_message(QueueUrl=sqs_queue, MessageBody=json.dumps(booking_data))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
