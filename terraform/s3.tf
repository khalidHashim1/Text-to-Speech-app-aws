# Terraform state File. 
resource "aws_s3_bucket" "terraformState" {
    bucket = "my-terraform-state-bucket-texttospeachapp"   
}

# Terraform state Versioning 
resource "aws_s3_bucket_versioning" "terraformStateVersioning" {
    bucket = aws_s3_bucket.terraformState.id

    versioning_configuration {
      status = "Enabled"
    }
}

# Terraform state public access 
resource "aws_s3_bucket_public_access_block" "terraformStatePublicAccess" {
    bucket = aws_s3_bucket.terraformState.id

    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}

#khalid-audio-converter1010 
resource "aws_s3_bucket" "khalidAudio" {
  bucket = "khalid-audio-converter1010"
}



