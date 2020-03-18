from aws_cdk import (
    core,
    aws_dynamodb as dynamodb,
)


class DynamoDBStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, reader_lambda, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._table = dynamodb.Table(
            self,
            "libraryTable",
            table_name="library",
            partition_key=dynamodb.Attribute(
                name="partition_key", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="added_at", type=dynamodb.AttributeType.STRING
            ),
        )

        self._table.add_global_secondary_index(
            index_name="partition_key-added_at-index",
            partition_key=dynamodb.Attribute(
                name="partition_key", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="added_at", type=dynamodb.AttributeType.STRING
            ),
        )

        self._table.grant_read_data(reader_lambda)

    @property
    def table(self):
        return self._table
