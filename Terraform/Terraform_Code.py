provider "aws" {
  region = "us-east-1"  # Cambia a tu región preferida
}

resource "aws_key_pair" "vockey" {
  key_name   = "vockey"
  public_key = file("~/.ssh/vockey.pub")  # Ruta a tu llave pública
}

resource "aws_security_group" "allow_ssh_http" {
  name        = "allow_ssh_http"
  description = "Permite trafico SSH (22) y HTTP (80)"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "dev_vm" {
  ami                         = "ami-0e68426dec8cb536b" # Aquí va el ID de la AMI "Cloud9ubuntu22"
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.vockey.key_name
  vpc_security_group_ids      = [aws_security_group.allow_ssh_http.id]
  associate_public_ip_address = true

  root_block_device {
    volume_size = 20
    volume_type = "gp2"
  }

  tags = {
    Name = "MV Desarrollo Terraform"
  }
}
