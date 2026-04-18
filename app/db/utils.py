from boto3.dynamodb.types import TypeDeserializer


def deserialize_dynamodb_item(item):
    deserializer = TypeDeserializer()
    if isinstance(item, list):
        return [deserialize_dynamodb_item(i) for i in item]
    elif isinstance(item, dict):
        # If this is a DynamoDB attribute value dict (e.g. {"S": "value"})
        if set(item.keys()) <= {"S", "N", "M", "L", "BOOL", "NULL"}:
            return deserializer.deserialize(item)
        # Otherwise, it's a regular dict
        return {k: deserialize_dynamodb_item(v) for k, v in item.items()}
    else:
        return item
