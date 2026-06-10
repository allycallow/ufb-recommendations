from app.db.consts import TABLE_NAME
from app.db.utils import deserialize_dynamodb_item, dynamodb


def get_trending_tracks():
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": "TRENDING#"},
            ":sk": {"S": "TRACK#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
        ScanIndexForward=False,
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]
