terraform {
  backend "s3" {
    bucket = "my-terraform-state-bucket-texttospeachapp"
    key    = "khalidhashim.com/terraform.tfstate" # temporary, overridden by backend-config
    region = "us-east-1"
    #dynamodb_table = "terraform-locks"
    encrypt = true
  }
}