from flask import Flask, render_template, request, jsonify, abort
from flask_cors import CORS  # Add this import
from werkzeug.utils import secure_filename
import requests
import os
import mimetypes
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("HUGGING_FACE_API_URL")
headers = {
    'Authorization': f'Bearer {os.getenv("HUGGING_FACE_API_KEY")}'
}

app = Flask(__name__)
CORS(app)  # Enable CORS

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit

def query(file):
    try:
        file_bytes = file.read()
        headers_with_type = headers.copy()
        headers_with_type['Content-Type'] = file.mimetype
        print(f"Sending request to {API_URL}")  # Debug log
        response = requests.post(
            API_URL,
            headers=headers_with_type,
            data=file_bytes
        )
        print(f"Response status: {response.status_code}")  # Debug log
        return response.json()
    except Exception as e:
        print(f"Error in query: {str(e)}")  # Debug log
        return {'error': f'Error processing request: {str(e)}'}

@app.route('/')
def index():
    return render_template('index.html')  # Remove the './' prefix

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file1' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file1']
    
    if not file or not file.filename:
        return jsonify({'error': 'No file selected'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
        
    try:
        modeldata = query(file)
        return jsonify(modeldata)
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': 'Error processing file'}), 500

if __name__ == '__main__':
    print("🌭 Starting Local Hot Dog Detector server...")
    print("Visit http://localhost:3000 in your browser")
    app.debug = True
    app.run(host='localhost', port=3000)