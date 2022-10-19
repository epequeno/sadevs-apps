from sadevs_apps.core_resources_stack import CoreResourcesStack
from aws_cdk import (
    Stack,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_s3_deployment as s3_deployment,
    aws_certificatemanager as certificate_manager,
)
from constructs import Construct


class CFrontStaticSiteStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        certificate_arn: str,
        hosted_zone_id,
        domain_name,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "HostedZone", hosted_zone_id=hosted_zone_id, zone_name=domain_name
        )

        # since the bucket has already been created from previous deployments
        # we build the bucket object from attributes here rather than creating a
        # new bucket.
        # This change is required since we had to re-create this entire stack
        # after the bucket had been originally created.
        site_bucket = s3.Bucket.from_bucket_attributes(
            self, "SiteBucket", bucket_name=domain_name
        )

        oai = cloudfront.OriginAccessIdentity(self, "OriginAccessIdentity")
        viewer_certificate = cloudfront.ViewerCertificate.from_acm_certificate(
            certificate_manager.Certificate.from_certificate_arn(
                self, "Certificate", certificate_arn=certificate_arn
            ),
            aliases=[domain_name],
        )

        distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "SiteDistribution",
            viewer_certificate=viewer_certificate,
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=site_bucket, origin_access_identity=oai
                    ),
                    behaviors=[cloudfront.Behavior(is_default_behavior=True)],
                ),
            ],
        )

        # noinspection PyTypeChecker
        route53.ARecord(
            self,
            "SiteAliasRecord",
            record_name=domain_name,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(distribution)
            ),
            zone=hosted_zone,
        )

        s3_deployment.BucketDeployment(
            self,
            "DeployWithInvalidation",
            sources=[s3_deployment.Source.asset("assets/elm/dst")],
            destination_bucket=site_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )
