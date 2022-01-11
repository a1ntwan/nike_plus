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
