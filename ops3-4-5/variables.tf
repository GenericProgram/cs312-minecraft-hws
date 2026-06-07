variable "aws_region" {
  default = "us-east-1"
}

variable "instance_type" {
  # Upgraded from t3.medium (4GB) to t3.large (8GB) for Ops 5.
  # Minecraft uses ~2.5Gi; Prometheus + Grafana + node-exporter need ~500MB.
  # t3.large provides comfortable headroom without risk of OOM during drills.
  default = "t3.large"
}

variable "key_name" {
  description = "The name of your AWS SSH key pair"
  type        = string
}

variable "private_key_path" {
  description = "The local path to your .pem file for Ansible/SSH access"
  type        = string
}

variable "ssh_allowed_cidr" {
  description = "Your IP in CIDR notation for SSH access restriction (e.g. 1.2.3.4/32)"
  type        = string
}
