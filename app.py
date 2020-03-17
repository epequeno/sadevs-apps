#!/usr/bin/env python3

from aws_cdk import core
import os

from sadevs_apps.core_resources_stack import CoreResourcesStack
from sadevs_apps.apigw_stack import ApiGwStack
from sadevs_apps.static_site_stack import CFrontStaticSiteStack

stack_env = env = core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-east-1",
)

app = core.App()

core_resources = CoreResourcesStack(app, "core-resources", env=stack_env,)

apps_stack = ApiGwStack(
    app,
    "apigw",
    acm_certificate=core_resources.certificate,
    hosted_zone=core_resources.hosted_zone,
    domain_name=core_resources.domain_name,
    env=stack_env,
)

CFrontStaticSiteStack(
    app,
    "cfront-static-site",
    certificate_arn=core_resources.certificate.certificate_arn,
    hosted_zone_id=core_resources.hosted_zone.hosted_zone_id,
    domain_name=core_resources.domain_name,
    env=stack_env,
)

app.synth()
