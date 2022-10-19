from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class DynamoDBStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._table = dynamodb.Table(
            self,
            "libraryTable",
            table_name="library",
            partition_key=dynamodb.Attribute(
                name="partition_key", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp", type=dynamodb.AttributeType.STRING
            ),
        )

        self._table.add_global_secondary_index(
            index_name="partition_key-timestamp-index",
            partition_key=dynamodb.Attribute(
                name="partition_key", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp", type=dynamodb.AttributeType.STRING
            ),
        )

    @property
    def table(self):
        return self._table
