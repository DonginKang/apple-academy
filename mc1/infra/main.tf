provider "aws" {
  region = "ap-northeast-2" # 서울 리전
}

data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "apple-dev-state-bucket"
    key    = "vpc/state.tfstate"
    region = "ap-northeast-2"
  }
}

# EC2 인스턴스 생성
resource "aws_instance" "apple-mc1-flask-dev" {
  ami                         = "ami-0d3d9b94632ba1e57" # Ubuntu Server 20.04 LTS AMI ID
  instance_type               = "t2.micro"
  key_name                    = "apple-dev"
  #associate_public_ip_address = true
  subnet_id                   = data.terraform_remote_state.vpc.outputs.public_subnet1_id
  security_groups             = [data.terraform_remote_state.vpc.outputs.security_group_id]

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
  }

  tags = {
    Name = "apple-mc1-flask-dev"
  }

}

data "aws_eip" "apple" {
  tags = {
    Name = "apple"
  }
}

# Elastic IP와 EC2 인스턴스 연결
resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.apple-mc1-flask-dev.id
  allocation_id = data.aws_eip.apple.id
}
