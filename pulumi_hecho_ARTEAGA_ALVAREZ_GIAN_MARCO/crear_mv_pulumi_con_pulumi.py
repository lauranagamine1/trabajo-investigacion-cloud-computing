import pulumi
import pulumi_aws as aws

security_group = aws.ec2.SecurityGroup("sg_desarrollo",
    description="Permite acceso SSH (22) y HTTP (80)",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ]
)

instance = aws.ec2.Instance("mv-desarrollo-instance",
    ami="ami-0363234289a7b6202",
    instance_type="t2.micro",
    key_name="vockey",
    vpc_security_group_ids=[security_group.id],
    root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
        volume_size=20,
        volume_type="gp2",
    ),

    tags={
        "Name": "Crear-MV-Gian-Marco-Arteaga-Alvarez"
    },
    
)
pulumi.export("instance_id", instance.id)