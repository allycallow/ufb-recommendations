import boto3
from app.db.utils import deserialize_dynamodb_item
from app.db.consts import TABLE_NAME

dynamodb = boto3.client("dynamodb", region_name="eu-west-2")


def get_recommendations(user_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"USER#{user_id}"},
            ":sk": {"S": f"RECOMMENDATION#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]


def get_more_like_artist(user_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"USER#{user_id}"},
            ":sk": {"S": f"MORE_LIKE_ARTIST#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]


def get_more_like_release(user_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"USER#{user_id}"},
            ":sk": {"S": f"MORE_LIKE_RELEASE#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]


def get_explore(user_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"USER#{user_id}"},
            ":sk": {"S": f"RECOMMENDATION#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]
