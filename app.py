#!/usr/bin/env python3
"""
high-level application definition. Component stacks are imported and used here. This defines how various resources
tie together. We can think of CFN stacks when thinking about the classes used here. Each will define resources and can
optionally produce "outputs" which can be used as inputs to other stacks.
"""
# stdlib
import os

# 3rd party
from aws_cdk import core
from sadevs_apps.core_resources_stack import CoreResourcesStack
from sadevs_apps.apigw_stack import ApiGwStack
from sadevs_apps.static_site_stack import CFrontStaticSiteStack
from sadevs_apps.dynamodb_stack import DynamoDBStack
from sadevs_apps.rusty_ecs_stack import RustyEcsStack

# local


stack_env = core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-east-1",
)

app = core.App()

core_resources = CoreResourcesStack(app, "core-resources", env=stack_env)
dynamodb_stack = DynamoDBStack(app, "dynamodb", env=stack_env)

apigw_stack = ApiGwStack(
    app,
    "apigw",
    env=stack_env,
    acm_certificate=core_resources.certificate,
    hosted_zone=core_resources.hosted_zone,
    domain_name=core_resources.domain_name,
    dynamodb_table=dynamodb_stack.table,
)

cfront_static_site_stack = CFrontStaticSiteStack(
    app,
    "cfront-static-site",
    env=stack_env,
    certificate_arn=core_resources.certificate.certificate_arn,
    hosted_zone_id=core_resources.hosted_zone.hosted_zone_id,
    domain_name=core_resources.domain_name,
)

rusty_ecs_stack = RustyEcsStack(
    app,
    "rusty-ecs",
    env=stack_env,
    dynamodb_table=dynamodb_stack.table,
    slack_token_secret_arn=os.environ["SLACKBOT_TOKEN_ARN"],
)

app.synth()
