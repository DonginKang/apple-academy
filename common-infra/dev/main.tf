provider "aws" {
  region = "ap-northeast-2" # 서울 리전
}

terraform {
  backend "s3" {
    bucket = "apple-dev-state-bucket"
    key    = "vpc/state.tfstate"
    region = "ap-northeast-2"
  }
}


# VPC 생성
resource "aws_vpc" "apple-dev" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "apple-dev"
  }
}

# Public Subnets
resource "aws_subnet" "public_subnet1" {
  vpc_id                  = aws_vpc.apple-dev.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-northeast-2a"

  tags = {
    Name = "public-subnet1"
  }
}

resource "aws_subnet" "public_subnet2" {
  vpc_id                  = aws_vpc.apple-dev.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-northeast-2c"

  tags = {
    Name = "public-subnet2"
  }
}

# Private Subnets
resource "aws_subnet" "private_subnet1" {
  vpc_id            = aws_vpc.apple-dev.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "private-subnet1"
  }
}

resource "aws_subnet" "private_subnet2" {
  vpc_id            = aws_vpc.apple-dev.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "private-subnet2"
  }
}

# 인터넷 게이트웨이 생성
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.apple-dev.id

  tags = {
    Name = "apple-dev-igw"
  }
}

# Public 서브넷을 위한 라우트 테이블 생성
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.apple-dev.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-route-table"
  }
}

# 라우트 테이블과 Public 서브넷 연결
resource "aws_route_table_association" "public_subnet1_rta" {
  subnet_id      = aws_subnet.public_subnet1.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "public_subnet2_rta" {
  subnet_id      = aws_subnet.public_subnet2.id
  route_table_id = aws_route_table.public_route_table.id
}

# 보안 그룹 생성 (All Open)
resource "aws_security_group" "dave-all-open" {
  name        = "dave-all-open"
  description = "All traffic allowed"
  vpc_id      = aws_vpc.apple-dev.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


output "public_subnet1_id" {
  value = aws_subnet.public_subnet1.id
}

output "public_subnet2_id" {
  value = aws_subnet.public_subnet2.id
}

output "security_group_id" {
  value = aws_security_group.dave-all-open.id
}

