import boto3
import json
<<<<<<< HEAD
import os
import uuid
import base64
from botocore.exceptions import ClientError
=======
import uuid
>>>>>>> 664b06c592ef67f6f9a7b313c899ee312614c72c

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')

<<<<<<< HEAD
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'khliad-audio-converter1010')
=======
BUCKET_NAME = 'khliad-audio-converter1010'
>>>>>>> 664b06c592ef67f6f9a7b313c899ee312614c72c
MAX_TEXT_LENGTH = 3000
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST"
}
<<<<<<< HEAD
PRESIGNED_URL_EXPIRES_IN_SECONDS = 3600

ALLOWED_VOICES = {
    # English
    "Joanna",
    "Matthew",
    # Arabic (examples; availability depends on region/account)
    "Zeina",
    "Hala",
}

ALLOWED_ENGINES = {"standard", "neural"}
=======
>>>>>>> 664b06c592ef67f6f9a7b313c899ee312614c72c


def _make_response(status_code, body_dict):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(body_dict)
    }


def lambda_handler(event, context):
    print("Received Event:", json.dumps(event))  # Debugging Log

<<<<<<< HEAD
    # Handle CORS preflight
    method = event.get("httpMethod")
    if not method:
        method = (event.get("requestContext", {}).get("http", {}) or {}).get("method")
    if method == "OPTIONS":
        return _make_response(200, {"ok": True})

    # Parse event body if using API Gateway
    try:
        if 'body' in event:
            raw_body = event.get('body') or "{}"
            if event.get("isBase64Encoded"):
                raw_body = base64.b64decode(raw_body).decode("utf-8")
            event_body = json.loads(raw_body) if isinstance(raw_body, str) else (raw_body or {})
        else:
            event_body = event or {}
    except (TypeError, json.JSONDecodeError) as e:
        print("Error parsing event body:", str(e))
        return _make_response(400, {'error': 'Invalid JSON body'})

    text = event_body.get('text', 'Hello, welcome to AWS Polly!')
    voice_id = (event_body.get("voiceId") or "Joanna").strip()
    engine = (event_body.get("engine") or "standard").strip().lower()
    output_format = (event_body.get("outputFormat") or "mp3").strip().lower()

=======
    # Parse event body if using API Gateway
    try:
        if 'body' in event:
            raw_body = event.get('body') or "{}"
            event_body = json.loads(raw_body)
        else:
            event_body = event or {}
    except (TypeError, json.JSONDecodeError) as e:
        print("Error parsing event body:", str(e))
        return _make_response(400, {'error': 'Invalid JSON body'})

    text = event_body.get('text', 'Hello, welcome to AWS Polly!')

>>>>>>> 664b06c592ef67f6f9a7b313c899ee312614c72c
    if not text or not str(text).strip():
        return _make_response(400, {'error': 'Missing "text" parameter'})

    text = str(text)
    if len(text) > MAX_TEXT_LENGTH:
        return _make_response(
            400,
            {'error': f'Text is too long. Maximum length is {MAX_TEXT_LENGTH} characters.'}
        )
<<<<<<< HEAD

    if output_format != "mp3":
        return _make_response(400, {"error": 'Only "mp3" outputFormat is supported currently.'})

    if voice_id not in ALLOWED_VOICES:
        return _make_response(400, {"error": f'Unsupported voiceId "{voice_id}".'})

    if engine not in ALLOWED_ENGINES:
        return _make_response(400, {"error": f'Unsupported engine "{engine}".'})
=======
>>>>>>> 664b06c592ef67f6f9a7b313c899ee312614c72c

    # Generate speech with Polly
    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine=engine
        )
    except ClientError as e:
        print("Polly synthesize_speech error:", str(e))
        return _make_response(500, {"error": "Polly synthesis failed.", "detail": str(e)})

    if 'AudioStream' not in response:
        return _make_response(500, {'error': 'Polly did not return audio data'})

    audio_stream = response['AudioStream'].read()
    request_id = getattr(context, 'aws_request_id', str(uuid.uuid4()))
    file_name = f'tts-{request_id}.mp3'

    # Upload to S3 (private). Return a presigned URL for access.
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=audio_stream,
            ContentType='audio/mpeg'
        )
    except ClientError as e:
        print("S3 put_object error:", str(e))
        return _make_response(500, {"error": "Failed to upload audio to S3.", "detail": str(e)})

    try:
        audio_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": file_name},
            ExpiresIn=PRESIGNED_URL_EXPIRES_IN_SECONDS
        )
    except ClientError as e:
        print("S3 generate_presigned_url error:", str(e))
        return _make_response(500, {"error": "Failed to generate audio URL.", "detail": str(e)})

    print("Generated Audio URL:", audio_url)  # Debugging Log

<<<<<<< HEAD
    return _make_response(
        200,
        {
            'audio_url': audio_url,
            'request_id': request_id,
            'expires_in': PRESIGNED_URL_EXPIRES_IN_SECONDS
        }
    )
=======
    return _make_response(200, {'audio_url': audio_url})
>>>>>>> 664b06c592ef67f6f9a7b313c899ee312614c72c
