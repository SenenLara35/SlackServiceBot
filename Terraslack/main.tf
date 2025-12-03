terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Cambia esto si usas otra región (ej: eu-west-1)
}

# 1. Buscamos la AMI de Ubuntu 22.04 (La más reciente)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical (Dueños de Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# 2. Security Group (El Firewall)
resource "aws_security_group" "slack_sg" {
  name        = "slack-service-sg"
  description = "Permitir SSH y FastAPI"

  # SSH (Puerto 22)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # FastAPI (Puerto 8000)
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Salida (Todo permitido)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. La Clave SSH (Sube tu clave pública a AWS)
resource "aws_key_pair" "deployer" {
  key_name   = "clave-slack-terraform"
  public_key = file("clave-slack.pub") # Asegúrate de que este archivo existe
}

# 4. La Máquina EC2
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro" # Capa gratuita
  key_name      = aws_key_pair.deployer.key_name
  
  vpc_security_group_ids = [aws_security_group.slack_sg.id]

  # Script de inicio (User Data) para instalar Python y Poetry automáticamente
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y python3-pip git
              
              # Instalar Poetry como usuario ubuntu (no root)
              su - ubuntu -c "curl -sSL https://install.python-poetry.org | python3-"
              su - ubuntu -c "echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc"
              EOF

  tags = {
    Name = "SlackBot-Server"
  }
}

# 5. Output (Para que nos diga la IP al terminar)
output "instance_ip" {
  value = aws_instance.app_server.public_ip
}