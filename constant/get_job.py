import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource("dynamodb")
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
table3 = dynamodb.Table("total_info")
table1 = dynamodb.Table("crawling_results")
table2 = dynamodb.Table("scraping_results")

def get_a_new_job(task_status):
    # Key = {"task_status": task_status}
    response = table1.query(
        IndexName="status-date-index",
        KeyConditionExpression=Key("job_status").eq(task_status), Limit=10
    )
    # print(response['Items'])
    return response['Items']

status = "scrapped"
print(get_a_new_job(status))
