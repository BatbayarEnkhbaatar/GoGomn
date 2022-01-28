import datetime

import boto3

from datetime import date, timedelta

dynamodb = boto3.resource("dynamodb")
table1 = dynamodb.Table("scraping_info")


def put_items_last_scraped(web_site_name, last_scrapped, links_no):
    response = table1.put_item(
        Item={
            'target_name': web_site_name,
            's_date': last_scrapped,
            'links_no': links_no
         }
    )
    return response
# website_name = "gogomn"
# link_no= "0"
# last_scrapped = (datetime.datetime.now() - timedelta(days=0)).strftime('%Y-%m-%d %H:%M')
# put_items_last_scraped(website_name, str(last_scrapped), link_no)