variable "AWS_REGION" {
  type = string
}

variable "profile" {
  default = "default"
  type = string 
}

variable "S3_NAME" {
  type = string
}

variable "EC2_AMI" {
  type = string
}

variable "instance_type" {
  #default = "t3.xlarge"
  default = "t3.micro"
  type = string
}

variable "EC2_KEYPAIR" {
  type = string
}

variable "EC2_COUNT" {
  type = number
}
