import boto3
import uuid
from datetime import date, timedelta
import shortuuid as shortuuid
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource("dynamodb")
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
table1 = dynamodb.Table("last_scraped")


def put_items_last_scraped(target_id, web_site_name, last_scrapped):
    response = table1.put_item(
        Item={
            'target_id': target_id,
            'name': web_site_name,
            'last_scraped': last_scrapped
         }
    )
    return response
random_id = uuid.uuid4()
short_id = shortuuid.encode(random_id)
target_id = short_id[:4]
website_name = "gogomn"
last_scrapped = (date.today() - timedelta(days=3)).strftime('%Y-%m-%d-%H-%M-%S')
put_items_last_scraped(target_id, website_name, str(last_scrapped))
