#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack


app = cdk.App()
CdkStack(app, "CdkStack",
     env=cdk.Environment(account="619874379465", region="us-east-1"),
    # Use custom synthesizer with minimal requirements
    synthesizer=cdk.DefaultStackSynthesizer(
        qualifier="labenv",
        file_assets_bucket_name="cdk-hnb659fds-assets-619874379465-us-east-1",
        deploy_role_arn="arn:aws:iam::619874379465:role/LabRole",
        cloud_formation_execution_role="arn:aws:iam::619874379465:role/LabRole",
        lookup_role_arn="arn:aws:iam::619874379465:role/LabRole",
        file_assets_publishing_role_arn="arn:aws:iam::619874379465:role/LabRole",
        image_assets_publishing_role_arn="arn:aws:iam::619874379465:role/LabRole"
    )
)

app.synth()
