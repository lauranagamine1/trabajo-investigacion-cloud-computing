from aws_cdk import App, Environment, DefaultStackSynthesizer
from cdk.cdk_stack import CdkStack
import boto3

# Obtener cuenta y región actuales
session = boto3.session.Session()
account_id = boto3.client('sts').get_caller_identity()['Account']
region = session.region_name

# Parámetros de despliegue
env = Environment(account=account_id, region=region)

# Crear app CDK
app = App()

# Configurar el sintetizador (para roles y assets)
synthesizer = DefaultStackSynthesizer(
    cloud_formation_execution_role=f"arn:aws:iam::{account_id}:role/LabRole",
    file_assets_bucket_name=f"cdk-hnb659fds-assets-{account_id}-{region}"
)

# Instanciar el stack
CdkStack(app, "CDKStack", env=env, synthesizer=synthesizer)

# Sintetizar 
app.synth()
