from app.db.consts import TABLE_NAME
from app.db.utils import deserialize_dynamodb_item, dynamodb


def get_playlist_suggested_tracks(playlist_id: str):
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "PK": {"S": f"PLAYLIST#{playlist_id}"},
            "SK": {"S": "SUGGESTED_TRACKS"},
        },
    )
    item = response.get("Item")
    if not item:
        return []
    deserialized = deserialize_dynamodb_item(item)
    return deserialized.get("items", [])
