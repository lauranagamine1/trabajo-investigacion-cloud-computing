from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Buscar la VPC por defecto
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # Crear grupo de seguridad para permitir SSH y HTTP
        sg = ec2.SecurityGroup(self, "SGCloud9Ubuntu",
            vpc=vpc,
            description="Permitir SSH y HTTP",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Permitir SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Permitir HTTP")

        # AMI Ubuntu 22.04 (en us-east-1)
        ami_id = "ami-043cbf1cf918dd74f"

        # Usar un par de claves existente (forma recomendada)
        key_pair = ec2.KeyPair.from_key_pair_name(
            self, "KeyPair", "vockey"
        )

        # Crear la instancia EC2
        ec2.Instance(self, "EC2Cloud9Ubuntu",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": ami_id
            }),
            vpc=vpc,
            security_group=sg,
            key_pair=key_pair,  # en lugar de key_name
            role=iam.Role.from_role_arn(self, "ExistingRole",
                "arn:aws:iam::619874379465:role/LabRole",
                mutable=False
            ),
            block_devices=[ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )]
        )
