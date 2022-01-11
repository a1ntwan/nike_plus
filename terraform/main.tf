provider "aws" {
  region      = var.AWS_REGION
  profile     = var.profile
} 


resource "aws_s3_bucket" "s3" {
  bucket                 = var.S3_NAME
  acl                    = "private"
  
  tags = {
    Name = var.S3_NAME
  }
}


resource "aws_instance" "ec2" {
  ami                    = var.EC2_AMI
  instance_type          = var.instance_type
  key_name               = var.EC2_KEYPAIR
  count                  = var.EC2_COUNT
  security_groups        = [aws_default_security_group.default_security_group.id]
  subnet_id              = aws_subnet.main.id
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
}
