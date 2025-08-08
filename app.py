from flask import Flask, request, jsonify
import boto3, uuid, os

app = Flask(__name__)
s3 = boto3.client('s3')

@app.route('/up', methods=['GET'])
def health_check():
    return jsonify({"status": "200 OK"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error":"No file provided"}), 400

    bucket = os.environ['S3_BUCKET']
    key = f"{uuid.uuid4()}_{file.filename}"
    s3.upload_fileobj(file, bucket, key)
    return jsonify({"url": f"https://{bucket}.s3.amazonaws.com/{key}"}), 200

@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    bucket = os.environ['S3_BUCKET']
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': filename},
        ExpiresIn=3600
    )
    return jsonify({"download_url": url}), 200

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
