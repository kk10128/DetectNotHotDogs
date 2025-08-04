 
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("HUGGING_FACE_API_URL")
headers = {'Authorization': f'Bearer {os.getenv("HUGGING_FACE_API_KEY")}'}

app = Flask(__name__)

def query(file):
    file_bytes = file.read()
    headers_with_type = headers.copy()
    headers_with_type['Content-Type'] = file.mimetype
    response = requests.post(
        API_URL,
        headers=headers_with_type,
        data=file_bytes
    )
    try:
        return response.json()
    except Exception:
        return {'error': 'Invalid response from API', 'content': response.text}
@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file1']
    modeldata = query(file)
    return jsonify(modeldata)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)