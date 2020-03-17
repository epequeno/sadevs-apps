from aws_cdk import (
    core,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_s3_deployment as s3_deployment,
)


class CFrontStaticSiteStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
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

        site_bucket = s3.Bucket(
            self,
            "SiteBucket",
            bucket_name=domain_name,
            website_index_document="index.html",
            website_error_document="error.html",
        )

        oai = cloudfront.OriginAccessIdentity(self, "OriginAccessIdentity")

        distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "SiteDistribution",
            alias_configuration=cloudfront.AliasConfiguration(
                acm_cert_ref=certificate_arn, names=[domain_name],
            ),
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=site_bucket, origin_access_identity=oai
                    ),
                    behaviors=[cloudfront.Behavior(is_default_behavior=True)],
                ),
            ],
        )

        route53.ARecord(
            self,
            "SiteAliasRecord",
            record_name=domain_name,
            target=route53.AddressRecordTarget.from_alias(
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
