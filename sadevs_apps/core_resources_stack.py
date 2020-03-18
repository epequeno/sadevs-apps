from aws_cdk import (
    core,
    aws_route53 as route53,
    aws_certificatemanager as certificate_manager,
)


class CoreResourcesStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._domain_name = "sadevs.app"
        self._hosted_zone = route53.PublicHostedZone(
            self, "HostedZone", zone_name=self._domain_name
        )

        self._certificate = certificate_manager.Certificate(
            self,
            "sadevs-apps-cert",
            domain_name=self._domain_name,
            subject_alternative_names=[f"*.{self._domain_name}"],
            validation_method=certificate_manager.ValidationMethod.DNS,
        )

    @property
    def domain_name(self):
        return self._domain_name

    @property
    def certificate(self):
        return self._certificate

    @property
    def hosted_zone(self):
        return self._hosted_zone
