import json
import boto3


def read_db():
    ddb_client = boto3.client("dynamodb")
    res = ddb_client.query(
        TableName="library",
        IndexName="partition_key-added_at-index",
        Select="ALL_ATTRIBUTES",
        ScanIndexForward=False,
        KeyConditionExpression="partition_key = :partition AND added_at >= :t1",
        ExpressionAttributeValues={
            ":partition": {"S": "records"},
            ":t1": {"S": "2020"},
        },
    )
    return res


def to_apigw_response(db_response):
    items = []
    for db_item in db_response.get("Items"):
        item = {
            "user": db_item.get("user").get("S"),
            "added_at": db_item.get("added_at").get("S"),
            "url": db_item.get("url").get("S"),
        }
        items.append(item)

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"items": items}),
        "isBase64Encoded": False,
    }


def handler(_event, _context):
    res = read_db()
    return to_apigw_response(res)
