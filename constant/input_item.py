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

def input_last_scraped(target_id, name, number):

    table = dynamodb.Table("last_scraped")
    table.put_item(
        Item={
            'target_id': date,
            'object': name,
            'status': status,
            'total_page_number': number
            }
    )
    return table
