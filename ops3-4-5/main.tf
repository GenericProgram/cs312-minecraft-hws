# 1. Provider and Versioning
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

#AMI Lookup
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] #Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

#Using Default VPC
data "aws_vpc" "default" {
  default = true
}

# Security Group: SSH (restricted) and Minecraft only
resource "aws_security_group" "minecraft_sg" {
  name        = "minecraft_security_group_ops4"
  description = "Allow SSH from known source and Minecraft traffic"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH from known IP only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  ingress {
    description = "Minecraft Server"
    from_port   = 25565
    to_port     = 25565
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

#The EC2 Instance, bootstrapped via Ansible (k3s + manifests)
resource "aws_instance" "minecraft_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name

  #AWS Academy IAM Profile, used for ECR pulls and S3 backup, no hardcoded creds
  iam_instance_profile = "LabInstanceProfile"

  vpc_security_group_ids = [aws_security_group.minecraft_sg.id]

  #20GB gp3, holds k3s, containerd image cache, and local-path PV data
  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  tags = {
    Name = "Minecraft-k3s-Server"
  }

  #Wait for SSH to be available before handing off to Ansible
  provisioner "remote-exec" {
    inline = ["echo 'Server is up and reachable'"]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.public_ip
    }
  }
}

#Ansible: installs k3s, restores S3 world data, applies K8s manifests
resource "null_resource" "ansible_trigger" {
  depends_on = [aws_instance.minecraft_server]

  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i '${aws_instance.minecraft_server.public_ip},' -u ubuntu --private-key ${var.private_key_path} playbook.yml"
  }
}

output "server_public_ip" {
  value       = aws_instance.minecraft_server.public_ip
  description = "The public IP of the Minecraft k3s server"
}
