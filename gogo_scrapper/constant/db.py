import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource("dynamodb")
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
table3 = dynamodb.Table("total_info")
table1 = dynamodb.Table("crawling_results")
table2 = dynamodb.Table("scraping_results")
table4 = dynamodb.Table("scraping_info")
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

def put_items_scraping_results(job_id, status, titile, result, published_date, journalist_name ):
    response = table2.put_item(
        Item={
            'job_id': job_id,
            'result': status,
            'title': titile,
            'result_data': result,
            'date': published_date,
            'journalist' : journalist_name
        }
    )
    return response
def put_items_last_scraped(web_site_name, last_scrapped, number_of_info):
    response = table4.put_item(
        Item={
            'target_name': web_site_name,
            's_date': last_scrapped,
            'link_no': number_of_info
         }
    )
    return response

def get_last_scrapped(target_name):
    target = table4.query(
        IndexName="target_name-s_date-index",
        KeyConditionExpression=Key("target_name").eq(target_name), Limit =1, ScanIndexForward=False
    )
    # print(total["Items"])
    last_scraped_date_dic = target['Items'][0]
    last_scraped_date = last_scraped_date_dic["s_date"]
    return last_scraped_date
gogoapp_last = get_last_scrapped("gogoapp")
print("gogo last scrapped time: ", gogoapp_last)