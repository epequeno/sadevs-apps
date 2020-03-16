#!/usr/bin/env python3

from aws_cdk import core
import os

from sadevs_apps.sadevs_apps_stack import SadevsAppsStack
from sadevs_apps.static_site_stack import StaticSiteStack


app = core.App()
apps_stack = SadevsAppsStack(
    app,
    "sadevs-apps",
    env=core.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-east-1",
    ),
)
StaticSiteStack(
    app,
    "static-site",
    certificate_arn=apps_stack.certificate_arn,
    env=core.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-east-1",
    ),
)

app.synth()
