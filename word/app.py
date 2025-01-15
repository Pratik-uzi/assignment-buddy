from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import threading
from functools import partial
from w2hw import process_file

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# Define the upload and output folders
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'output')

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Track processing status
processing_status = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Start processing in background
        thread = threading.Thread(
            target=process_in_background,
            args=(file_path, OUTPUT_FOLDER, filename)
        )
        thread.start()

        return jsonify({
            "status": "processing",
            "message": "File is being processed",
            "check_status": f"/status/{filename}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status/<filename>')
def check_status(filename):
    status = processing_status.get(filename, "processing")
    if status == "completed":
        output_filename = f"handwritten_{os.path.splitext(filename)[0]}.pdf"
        processing_status.pop(filename, None)
        return jsonify({
            "status": "completed",
            "download_link": f"/download/{output_filename}"
        })
    elif status == "error":
        error = processing_status.pop(filename, None)
        return jsonify({"status": "error", "error": str(error)}), 500
    else:
        return jsonify({"status": "processing"})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(OUTPUT_FOLDER, filename),
        as_attachment=True,
        download_name=filename
    )

def process_in_background(file_path, output_folder, filename):
    try:
        process_file(file_path, output_folder)
        processing_status[filename] = "completed"
    except Exception as e:
        processing_status[filename] = f"error: {str(e)}"
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)