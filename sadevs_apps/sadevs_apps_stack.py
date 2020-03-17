from aws_cdk import (
    core,
    aws_apigateway as apigw,
    aws_lambda,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)


class ApiGwStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        acm_certificate,
        hosted_zone,
        domain_name,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        hello_lambda = aws_lambda.Function(
            self,
            "HelloHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset("assets/lambda/hello"),
            handler="hello.handler",
        )

        gw = apigw.LambdaRestApi(self, "ApiGw", handler=hello_lambda)
        gw_domain = gw.add_domain_name(
            "GWDomainName",
            certificate=acm_certificate,
            domain_name=f"api.{domain_name}",
        )

        route53.ARecord(
            self,
            "ApiGwARecord",
            record_name="api",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.ApiGatewayDomain(gw_domain)
            ),
        )
