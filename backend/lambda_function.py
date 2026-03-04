import boto3
import json
import uuid

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')

BUCKET_NAME = 'khalid-audio-converter1010'  # keep this private
MAX_TEXT_LENGTH = 3000
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST"
}

def _make_response(status_code, body_dict):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(body_dict)
    }

def lambda_handler(event, context):
    print("Received Event:", json.dumps(event))

    # Handle CORS preflight
    method = event.get("httpMethod") or (event.get("requestContext", {}).get("http", {}) or {}).get("method")
    if method == "OPTIONS":
        return _make_response(200, {"ok": True})

    # Parse event body
    try:
        event_body = json.loads(event.get('body', '{}')) if 'body' in event else event or {}
    except (TypeError, json.JSONDecodeError) as e:
        print("Error parsing event body:", str(e))
        return _make_response(400, {'error': 'Invalid JSON body'})

    text = event_body.get('text', 'Hello, welcome to AWS Polly!')

    if not text.strip():
        return _make_response(400, {'error': 'Missing "text" parameter'})

    if len(text) > MAX_TEXT_LENGTH:
        return _make_response(
            400,
            {'error': f'Text is too long. Maximum length is {MAX_TEXT_LENGTH} characters.'}
        )

    # Generate speech with Polly
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    if 'AudioStream' not in response:
        return _make_response(500, {'error': 'Polly did not return audio data'})

    audio_stream = response['AudioStream'].read()
    request_id = getattr(context, 'aws_request_id', str(uuid.uuid4()))
    file_name = f'tts-{request_id}.mp3'

    # Upload to private S3 bucket
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=audio_stream,
        ContentType='audio/mpeg'
    )

    # Generate a pre-signed URL (valid for 1 hour)
    audio_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': file_name},
        ExpiresIn=3600
    )

    print("Generated pre-signed Audio URL:", audio_url)

    return _make_response(200, {'audio_url': audio_url})
