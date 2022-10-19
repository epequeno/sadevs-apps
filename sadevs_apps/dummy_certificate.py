"""
when modifying the certificate from the core resources it is necessary to point resources that use the cert to another
certificate. This is intended to be a temporary resource while updating the core resources cert.
"""
# stdlib

# 3rd party
from aws_cdk import (
    Stack,
    aws_route53 as route53,
    aws_certificatemanager as certificate_manager,
)
from constructs import Construct

# local


class DummyCertificateStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._domain_name = "sadevs.app"
        self._hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "ProdCert", hosted_zone_id="Z2E93J3M5GN8BP", zone_name="sadevs.app"
        )
        self._certificate = certificate_manager.Certificate(
            self,
            "sadevs-apps-cert",
            domain_name=self._domain_name,
            subject_alternative_names=[f"*.{self._domain_name}"],
            validation=certificate_manager.CertificateValidation.from_dns(
                self._hosted_zone
            ),
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
