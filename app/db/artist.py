import boto3
from app.db.utils import deserialize_dynamodb_item
from app.db.consts import TABLE_NAME

dynamodb = boto3.client("dynamodb", region_name="eu-west-2")


def get_artist_related_artists(artist_id: str):
    response = dynamodb.query(
        TableName=TABLE_NAME,
        KeyConditionExpression="#pk = :pk And begins_with(#sk, :sk)",
        ExpressionAttributeValues={
            ":pk": {"S": f"ARTIST#{artist_id}"},
            ":sk": {"S": f"RELATED_ARTISTS#"},
        },
        ExpressionAttributeNames={
            "#pk": "PK",
            "#sk": "SK",
        },
    )
    items = response.get("Items", [])
    return [deserialize_dynamodb_item(item) for item in items]
