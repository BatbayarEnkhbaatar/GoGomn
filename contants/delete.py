import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource("dynamodb")
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
table3 = dynamodb.Table("total_info")
table1 = dynamodb.Table("crawling_results")
table2 = dynamodb.Table("scraping_results")


def delete_all():
    job_id = table1.query(AttributesToGet=['task_id'])
    # print(job_id['Items'])
    return job_id['Items']
