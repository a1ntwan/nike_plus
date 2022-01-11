resource "aws_vpc" "mainvpc" {
  cidr_block = "10.1.0.0/16"

  tags = {
    Name = "Default"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.mainvpc.id

  tags = {
    Name = "main"
  }
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.mainvpc.id
  cidr_block = "10.1.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "Nike"
  }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.mainvpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "main"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}
