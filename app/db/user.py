from app.db.consts import TABLE_NAME
from app.db.utils import deserialize_dynamodb_item, dynamodb


def get_recommendations(user_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        FilterExpression="NOT begins_with(#sk, :artist_sk) AND NOT begins_with(#sk, :release_sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"USER#{user_id}"},
            ":sk": {"S": "RECOMMENDATION#"},
            ":artist_sk": {"S": "RECOMMENDATION#ARTIST#"},
            ":release_sk": {"S": "RECOMMENDATION#RELEASE#"},
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
            ":sk": {"S": "RECOMMENDATION#ARTIST#"},
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
            ":sk": {"S": "RECOMMENDATION#RELEASE#"},
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
        FilterExpression="NOT begins_with(#sk, :artist_sk) AND NOT begins_with(#sk, :release_sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"USER#{user_id}"},
            ":sk": {"S": "RECOMMENDATION#"},
            ":artist_sk": {"S": "RECOMMENDATION#ARTIST#"},
            ":release_sk": {"S": "RECOMMENDATION#RELEASE#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]


def get_top_picks(user_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"USER#{user_id}"},
            ":sk": {"S": "TOP_PICKS#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]
