#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack


app = cdk.App()
CdkStack(app, "CdkStack",
     env=cdk.Environment(account="619874379465", region="us-east-1"),
    synthesizer=cdk.DefaultStackSynthesizer(
        qualifier="labenv",
        # Use existing execution role
        deploy_role_arn="arn:aws:iam::619874379465:role/LabRole",
        cloud_formation_execution_role="arn:aws:iam::619874379465:role/LabRole"
    )
)

app.synth()
