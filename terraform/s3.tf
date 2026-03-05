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

resource "aws_s3_bucket_public_access_block" "khalidAudio" {
    bucket = aws_s3_bucket.khalidAudio.id

    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}

# texttospeach.khalidhashim.com
resource "aws_s3_bucket" "khalidStaticSite" {
  bucket = "texttospeach.khalidhashim.com"

  tags = {
    awsApplication = "arn:aws:resource-groups:us-east-1:665832050840:group/khalidhashimCV-WebApplication/04ydkgutdg9qdvdnu1jjvbmipe"
  }
}

# texttospeach.khalidhashim.com  Versioning 
resource "aws_s3_bucket_versioning" "khalidStaticSiteVersioning" {
    bucket = aws_s3_bucket.khalidStaticSite.id

    versioning_configuration {
      status = "Enabled"
    }
}
# texttospeach.khalidhashim.com  public access
resource "aws_s3_bucket_public_access_block" "khalidPublicAccess" {
    bucket = aws_s3_bucket.khalidStaticSite.id

    block_public_acls = false
    block_public_policy = false
    ignore_public_acls = false
    restrict_public_buckets = false
}

