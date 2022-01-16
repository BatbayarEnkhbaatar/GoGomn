import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamodb = boto3.resource("dynamodb")
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
table3 = dynamodb.Table("total_info")
table1 = dynamodb.Table("crawling_results")
table2 = dynamodb.Table("scraping_results")


def getitem_all():
    job_id = table1.query(AttributesToGet=['task_id'])
    # print(job_id['Items'])
    return job_id['Items']


# item_list = getitem_all()
# for item in item_list:
#     print(item)

def get_an_item(task_status):
    # Key = {"task_status": task_status}
    response = table1.query(
        IndexName="task_status-index",
        KeyConditionExpression=Key("task_status").eq(task_status), Limit=1
    )
    # print(response['Items'])
    return response['Items']


def get_count_item(task_status):
    total = table1.query(
        IndexName="task_status-index",
        KeyConditionExpression=Key("task_status").eq(task_status)
    )
    # print(total["Items"])
    return len(total["Items"])


def update_item(task_id, job_id, n_status, xpath_link, rule_data):
    response = table2.update_item(
        Key={
            'task_id': task_id,
            'job_id': job_id
        },
        UpdateExpression="set task_status=:new_status, xpath_link=:new_xpath, rule_data=:new_rule_data",
        ExpressionAttributeValues={
            ':new_status': n_status,
            ':new_xpath': xpath_link,
            ':new_rule_data': rule_data
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def put_items_crawling_results(job_id, status, link):
    response = table1.put_item(
        Item={
            'job_id': job_id,
            'urls': {
                'status': status,
                'link': link
            }
        }
    )
    return response
def put_items_total_info(date, status, name, number):
    response = table1.put_item(
        Item={
            'date': date,
            'name': {
                'status': status,
                'target_website': name,
                'total_page_number': number
            }
        }
    )
    return response

# task_status = "Changed"
# print("Please enter task id: ")
# task_id = input()
#
# print("Please enter JOB ID: ")
# job_id = input()
# print("Please enter New Status: ")
# task_status = input()
# print("Please enter Xpath: ")
# xpath = input()
# print("Please enter Rule_Data ")
# rule = input()
# print(update_item(str(task_id), str(job_id), task_status, xpath, rule))
# print("it is updated")

#
# print("Please enter status: ")
# new_status = input()
# item_returned = get_count_item("ongoing")
# print(item_returned)

