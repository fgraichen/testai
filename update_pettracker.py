#create python funtion update_pettracker_table(prompt, result)  to update  dynamodb table named pettracker with a new entry with model_id = "claude" and DT = timestamp and  attribute prompt = prompt and attribute result = result
import boto3
import datetime
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def update_pettracker_table(prompt, result):    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pettracker')
    response = table.update_item(
        Key={
            'model_id': 'claude',
            'DT': str(datetime.datetime.now())
        },
        UpdateExpression="set prompt = :p, result = :r",
        ExpressionAttributeValues={
            ':p': prompt,
            ':r': result
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
#invoke the update_tracker_table with try catch logic   
    try:
        response = update_pettracker_table(prompt, result)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("UpdateItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))   