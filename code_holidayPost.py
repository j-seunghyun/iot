import json
import boto3
import base64
import binascii
from binascii import unhexlify

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Holiday')
    
    result = base64.b64decode(event.get('body')).decode('utf-8')
    keys = []
    values = []
    data_list = result.split("&")
    
    for data in data_list:
        pair = data.split("=")
        keys.append(pair[0])
        values.append(pair[1])
    
    my_dict = dict(zip(keys,values))
    imsiresult = my_dict['dateName']
    #hexlify 형태를 만들어 주기 위해 lower과 %문자 제거
    tmpvalue = imsiresult.lower()
    tmp = tmpvalue.replace('%', '')
    #unhexlify함수를 사용해 byte code로 만든 후 다시 utf-8방식으로 decode
    my_dict['dateName'] = unhexlify(tmp).decode('utf-8')
    
    data =table.put_item(
        Item={
            'date': int(my_dict['locdate']),
            'sortdate': int(my_dict['sortdate']),
            'holiday': my_dict['dateName']
        }
    )
    return response

