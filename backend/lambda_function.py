import boto3
import json
import uuid

# AWS clients
polly_client = boto3.client("polly")
s3_client = boto3.client("s3")

# Constants
BUCKET_NAME = "khalid-audio-converter1010"
MAX_TEXT_LENGTH = 3000
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST"
}


def _make_response(status_code, body_dict):
    """Helper to create API Gateway compatible response"""
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body_dict)
    }


def lambda_handler(event, context):
    print("Received Event:", json.dumps(event))

    # Handle CORS preflight
    method = event.get("httpMethod") or (event.get("requestContext", {}).get("http", {}) or {}).get("method")
    if method == "OPTIONS":
        return _make_response(200, {"ok": True})

    # Parse body
    try:
        raw_body = event.get("body") or "{}"
        event_body = json.loads(raw_body)
    except (TypeError, json.JSONDecodeError) as e:
        print("Error parsing event body:", str(e))
        return _make_response(400, {"error": "Invalid JSON body"})

    text = event_body.get("text", "").strip()
    if not text:
        return _make_response(400, {"error": 'Missing "text" parameter'})
    if len(text) > MAX_TEXT_LENGTH:
        return _make_response(400, {"error": f"Text too long. Max {MAX_TEXT_LENGTH} chars."})

    # Generate speech with Polly
    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna"
        )
        audio_stream = response.get("AudioStream").read()
    except Exception as e:
        print("Polly error:", e)
        return _make_response(500, {"error": "Error generating speech"})

    # Create unique file name
    request_id = getattr(context, "aws_request_id", str(uuid.uuid4()))
    file_name = f"tts-{request_id}.mp3"

    # Upload to private S3 (no public ACL)
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=audio_stream,
            ContentType="audio/mpeg"
        )
    except Exception as e:
        print("S3 upload error:", e)
        return _make_response(500, {"error": "Error saving audio file"})

    # Generate pre-signed URL (valid for 1 hour)
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": file_name},
            ExpiresIn=3600  # seconds
        )
    except Exception as e:
        print("Pre-signed URL error:", e)
        return _make_response(500, {"error": "Error generating audio URL"})

    print("Generated Pre-signed URL:", presigned_url)

    return _make_response(200, {"audio_url": presigned_url})
