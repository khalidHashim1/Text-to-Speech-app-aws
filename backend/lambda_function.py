import json
import boto3
import uuid
import os

# Initialize clients
polly_client = boto3.client("polly")
s3_client = boto3.client("s3")

BUCKET_NAME = "khalid-audio-converter1010"  # your private bucket

def lambda_handler(event, context):
    try:
        # Parse input text
        body = json.loads(event.get("body", "{}"))
        text = body.get("text", "").strip()
        
        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Text is required"})
            }

        # Generate speech with Polly
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna"  # choose any supported voice
        )

        # Create a unique S3 object key
        file_key = f"tts-{uuid.uuid4()}.mp3"

        # Upload audio to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=response['AudioStream'].read()
        )

        # Generate a pre-signed URL valid for 1 hour
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_key},
            ExpiresIn=3600  # 1 hour
        )

        # Return the URL to frontend
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # for CORS
            },
            "body": json.dumps({"audio_url": presigned_url})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Failed to generate speech", "details": str(e)})
        }
