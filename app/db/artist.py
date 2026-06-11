from app.db.consts import TABLE_NAME
from app.db.utils import deserialize_dynamodb_item, dynamodb


def get_artist_related_artists(artist_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"ARTIST#{artist_id}"},
            ":sk": {"S": "RELATED_ARTISTS#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]


def get_trending_artists():
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "PK": {"S": "TRENDING#ARTISTS"},
            "SK": {"S": "LATEST"},
        },
    )
    item = response.get("Item")
    if not item:
        return []
    deserialized = deserialize_dynamodb_item(item)
    return deserialized.get("items", [])
