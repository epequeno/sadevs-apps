#!/usr/bin/env python3

from aws_cdk import core
import os

from sadevs_apps.sadevs_apps_stack import SadevsAppsStack


app = core.App()
SadevsAppsStack(
    app,
    "sadevs-apps",
    env=core.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-east-1",
    ),
)

app.synth()
