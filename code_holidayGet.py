import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

#because Decimal object cannot transformed into json string
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self,obj)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Holiday')
    
    sortdict = event.get('queryStringParameters')
    sortdate = sortdict['sortdate']
    
    data =table.query(
        KeyConditionExpression=Key('sortdate').eq(int(sortdate))
    )
    response = {
        'statusCode': 200,
        'body': json.dumps(data.get('Items'), cls=DecimalEncoder)
    }
    return response
