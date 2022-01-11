resource "aws_iam_role_policy" "s3_access" {
  name = "s3_access"
  role = aws_iam_role.bucket_access.id

  policy = file("ec2-policy.json")
}

resource "aws_iam_role" "bucket_access" {
  name = "bucket_access"

  assume_role_policy = file("ec2-assume-policy.json")
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.bucket_access.name
}
