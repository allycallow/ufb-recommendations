from app.db.consts import TABLE_NAME
from app.db.utils import deserialize_dynamodb_item, dynamodb


def get_trending_tracks():
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "PK": {"S": "TRENDING#TRACKS"},
            "SK": {"S": "LATEST"},
        },
    )
    item = response.get("Item")
    if not item:
        return []
    deserialized = deserialize_dynamodb_item(item)
    return deserialized.get("items", [])
