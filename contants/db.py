import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource("dynamodb")
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
table3 = dynamodb.Table("total_info")
table1 = dynamodb.Table("crawling_results")
table2 = dynamodb.Table("scraping_results")
table4 = dynamodb.Table("last_scraped")
def getitem_all():
    job_id = table1.query(AttributesToGet=['task_id'])
    # print(job_id['Items'])
    return job_id['Items']

def get_a_new_job(task_status):
    response = table1.query(
        IndexName="status-date-index",
        KeyConditionExpression=Key("job_status").eq(task_status), Limit=1
    )
    return response['Items']

def update_crawling_results(job_id, new_status, link, date):
    response = table1.update_item(
        Key={
            'job_id': job_id,
            'job_url': link
        },
        UpdateExpression="SET job_status=:n_status, inserted_date=:date_in",
        ExpressionAttributeValues={
            ':n_status': new_status,
            ':date_in': date
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def get_count_item(task_status):
    total = table1.query(
        IndexName="status-date-index",
        KeyConditionExpression=Key("job_status").eq(task_status)
    )
    # print(total["Items"])
    return len(total["Items"])

def put_items_crawling_results(job_id, status, link, date):
    response = table1.put_item(
        Item={
            'job_id': job_id,
            'job_url': link,
            'job_status': status,
            'inserted_date': date
        }
    )
    return response

def put_items_scraping_results(job_id, status, titile, result, published_date ):
    response = table2.put_item(
        Item={
            'job_id': job_id,
            'result': status,
            'title': titile,
            'result_data': result,
            'date': published_date
        }
    )
    return response
def put_last_scraped_time(target_website, last_execution):
    response = table2.put_item(
        Item={
            'target_website': target_website,
            'last_scraped_time': last_execution,
        }
    )
    return response
def put_items_total_info(date, status, name, number):
    response = table3.put_item(
        Item={
            'object': name,
            'total_page_number': number
            }
    )
    return response

<<<<<<< HEAD
=======

>>>>>>> f733b80fb015049b471bc581d68d9b2e64463e1a

