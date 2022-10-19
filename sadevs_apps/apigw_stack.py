"""
defines the API gateway and associated lambdas
"""
# stdlib

# 3rd party
from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)
from constructs import Construct

# local


class ApiGwStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        acm_certificate,
        hosted_zone,
        domain_name,
        dynamodb_table,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        db_get_lambda = aws_lambda.Function(
            self,
            "dbGet",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset("assets/lambda/db_get"),
            handler="db_get.handler",
        )

        self._db_get_lambda = db_get_lambda

        gw = apigw.LambdaRestApi(self, "ApiGw", handler=db_get_lambda)
        gw_domain = gw.add_domain_name(
            "GWDomainName",
            certificate=acm_certificate,
            domain_name=f"api.{domain_name}",
        )

        # noinspection PyTypeChecker
        route53.ARecord(
            self,
            "ApiGwARecord",
            record_name="api",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.ApiGatewayDomain(gw_domain)
            ),
        )

        dynamodb_table.grant_read_data(self._db_get_lambda)

    @property
    def db_get_lambda(self):
        return self._db_get_lambda
