from app.db.consts import TABLE_NAME
from app.db.utils import deserialize_dynamodb_item, dynamodb


def get_artist_related_artists(artist_id: str):
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "PK": {"S": f"ARTIST#{artist_id}"},
            "SK": {"S": f"RELATED_ARTISTS#{artist_id}"},
        },
    )
    item = response.get("Item")
    if not item:
        return []
    deserialized = deserialize_dynamodb_item(item)
    return deserialized.get("items", [])


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


def get_artist_top_picks(artist_id: str):
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "PK": {"S": f"ARTIST#{artist_id}"},
            "SK": {"S": "TOP_PICKS"},
        },
    )
    item = response.get("Item")
    if not item:
        return []
    deserialized = deserialize_dynamodb_item(item)
    return deserialized.get("items", [])
