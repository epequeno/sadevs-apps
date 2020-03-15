from aws_cdk import core, aws_apigateway as apigw, aws_lambda, aws_route53 as route53


class SadevsAppsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hosted_zone = route53.PublicHostedZone(
            self, "HostedZone", zone_name="sadevs.app"
        )

        hello_lambda = aws_lambda.Function(
            self,
            "HelloHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset("assets/lambda/hello"),
            handler="hello.handler",
        )

        gw = apigw.LambdaRestApi(self, "Endpoint", handler=hello_lambda)
