import pulumi
import pulumi_aws as aws

# 1. Obtener la VPC por defecto
vpc = aws.ec2.get_vpc(default=True)

# 2. Obtener la subred pública por defecto
subnet = aws.ec2.get_subnet(filters=[
    {"name": "vpc-id", "values": [vpc.id]},
    {"name": "availabilityZone", "values": ["us-east-1a"]},
])

# 3. Crear el grupo de seguridad permitiendo puertos 22 (SSH) y 80 (HTTP)
security_group = aws.ec2.SecurityGroup("my-security-group",
    vpc_id=vpc.id,
    description="Permitir SSH y HTTP",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            from_port=22,
            to_port=22,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            from_port=80,
            to_port=80,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
    ]
)

# 4. Buscar una AMI válida de Ubuntu 22.04 publicada por Canonical
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["099720109477"],  # Canonical
    filters=[
        {"name": "name", "values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]},
        {"name": "virtualization-type", "values": ["hvm"]},
    ]
)

# 5. Crear la instancia EC2 con la AMI, disco de 20GB, clave vockey
instance = aws.ec2.Instance("my-instance",
    ami=ami.id,
    instance_type="t2.micro",
    subnet_id=subnet.id,  # Usamos subnet_id correctamente aquí
    key_name="vockey",  # Asegúrate de que el nombre de la clave SSH coincida
    security_groups=[security_group.name],  # Usamos 'security_groups' en lugar de 'security_group_ids'
    root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
        volume_size=20,
        volume_type="gp2"
    ),
    tags={
        "Name": "MV Desarrollo"
    }
)

# 6. Exportar la IP pública
pulumi.export("public_ip", instance.public_ip)