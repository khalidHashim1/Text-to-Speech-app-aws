resource "aws_lambda_function" "mylambdaFunction" {
        function_name = "TextToSpeachFunction"
        role          = "arn:aws:iam::665832050840:role/service-role/TextToSpeachFunction-role-bos7yg5b"
        handler       = "lambda_function.lambda_handler"
        runtime       = "python3.13"
        publish       = false
        
        # Placeholder to satisfy Terraform requirement
        s3_bucket = "dummy-bucket-terraform-placeholder"
        s3_key    = "dummy.zip"

        lifecycle {
            ignore_changes = [filename, s3_bucket, s3_key]
        }
}


