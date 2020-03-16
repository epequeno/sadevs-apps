from aws_cdk import (
    core,
    aws_apigateway as apigw,
    aws_lambda,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_certificatemanager as certificate_manager,
)
from common import DOMAIN_NAME


class SadevsAppsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hosted_zone = route53.PublicHostedZone(
            self, "HostedZone", zone_name=DOMAIN_NAME
        )

        certificate = certificate_manager.DnsValidatedCertificate(
            self,
            "sadevs-apps-cert",
            hosted_zone=hosted_zone,
            domain_name=DOMAIN_NAME,
            subject_alternative_names=[f"*.{DOMAIN_NAME}"],
            validation_method=certificate_manager.ValidationMethod.DNS,
        )

        self._certificate_arn = certificate.certificate_arn

        hello_lambda = aws_lambda.Function(
            self,
            "HelloHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset("assets/lambda/hello"),
            handler="hello.handler",
        )

        gw = apigw.LambdaRestApi(self, "ApiGw", handler=hello_lambda)
        gw_domain = gw.add_domain_name(
            "GWDomainName", certificate=certificate, domain_name=f"api.{DOMAIN_NAME}"
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

    @property
    def certificate_arn(self):
        return self._certificate_arn
