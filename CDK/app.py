import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack


app = cdk.App()

CdkStack(app, "CdkStack",
     env=cdk.Environment(account="619874379465", region="us-east-1")
)

app.synth()

from aws_cdk import App, Environment, DefaultStackSynthesizer
from cdk_python.cdk_python_stack import PilaEc2
import boto3

session = boto3.session.Session()
account_id = boto3.client('sts').get_caller_identity()['Account']
region = session.region_name

qualifier = "ec2-dep"
app = App()

env = Environment(account=account_id, region=region)

sintetizador = DefaultStackSynthesizer(
qualifier=qualifier,
cloud_formation_execution_role=f"arn:aws:iam::{account_id}:role/LabRole",
file_assets_bucket_name=f"cdk-{qualifier}-assets-{account_id}-{region}"
)

PilaEc2(app, "PilaEc2", env=env, synthesizer=sintetizador)
app.synth()