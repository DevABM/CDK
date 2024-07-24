# lambda_function.py
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
primary_key = os.environ['PRIMARY_KEY']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Get the current visitor count
    response = table.get_item(Key={primary_key: 'visitor_count'})
    if 'Item' in response:
        count = response['Item']['count']
    else:
        count = 0

    # Increment the count
    new_count = count + 1

    # Update the count in the table
    table.put_item(Item={primary_key: 'visitor_count', 'count': new_count})

    return {
        'statusCode': 200,
        'body': f'Visitor count updated to {new_count}'
    }
