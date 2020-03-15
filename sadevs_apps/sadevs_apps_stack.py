from aws_cdk import core, aws_apigateway as apigw, aws_lambda


class SadevsAppsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hello_lambda = aws_lambda.Function(
            self,
            "HelloHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset("assets/lambda/hello"),
            handler="hello.handler",
        )

        gw = apigw.LambdaRestApi(self, "Endpoint", handler=hello_lambda)
