from app.db.consts import TABLE_NAME
from app.db.utils import deserialize_dynamodb_item, dynamodb


def get_label_related_artists(label_id: str):
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "PK": {"S": f"LABEL#{label_id}"},
            "SK": {"S": f"RELATED_ARTISTS#{label_id}"},
        },
    )
    item = response.get("Item")
    if not item:
        return []
    deserialized = deserialize_dynamodb_item(item)
    return deserialized.get("items", [])


def get_label_top_picks(label_id: str):
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "PK": {"S": f"LABEL#{label_id}"},
            "SK": {"S": "TOP_PICKS"},
        },
    )
    item = response.get("Item")
    if not item:
        return []
    deserialized = deserialize_dynamodb_item(item)
    return deserialized.get("items", [])
