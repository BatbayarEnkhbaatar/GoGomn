import boto3
from boto3.dynamodb.conditions import Attr, Key
dynamodb = boto3.resource("dynamodb")


def input_total_info(date, status, name, number):

    table = dynamodb.Table("total_info")
    table.put_item(
        Item={
            'date': date,
            'object': name,
            'status': status,
            'total_page_number': number
            }
    )
    return table
