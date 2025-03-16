import boto3
import json

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')

BUCKET_NAME = 'khliad-audio-converter1010'

def lambda_handler(event, context):
    print("Received Event:", json.dumps(event))  # Debugging Log

    # Parse event body if using API Gateway
    event_body = json.loads(event['body']) if 'body' in event else event
    text = event_body.get('text', 'Hello, welcome to AWS Polly!')

    if not text:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing "text" parameter'})
        }

    # Generate speech with Polly
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    if 'AudioStream' not in response:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Polly did not return audio data'})
        }

    audio_stream = response['AudioStream'].read()
    file_name = f'tts-{context.aws_request_id}.mp3'

    # Upload to S3 with public access
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=audio_stream,
        ContentType='audio/mpeg',
        ACL='public-read'
    )

    # Get AWS region
    region = boto3.session.Session().region_name
    audio_url = f"https://{BUCKET_NAME}.s3.{region}.amazonaws.com/{file_name}"

    print("Generated Audio URL:", audio_url)  # Debugging Log

    return {
        'statusCode': 200,
        'body': json.dumps({'audio_url': audio_url})
    }
