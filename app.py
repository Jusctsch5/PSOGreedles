from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import zipfile
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.zip'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                has_psobank = '.psobank' in zip_ref.namelist()
                pso_char_files = [f for f in zip_ref.namelist() if f.endswith('.psochar')]
                
                if not has_psobank:
                    return jsonify({'error': 'The zip file must contain exactly one .psobank file at the root.'}), 400
                
                # Process the files here
                parsed_data = {
                    'psobank': parse_psobank_file(zip_ref.read('.psobank')),
                    'psoChars': [parse_pso_char_file(zip_ref.read(f)) for f in pso_char_files]
                }
                
                return jsonify(parsed_data)
                
        except Exception as e:
            return jsonify({'error': f'Error processing zip file: {str(e)}'}), 400
        finally:
            # Clean up the uploaded file
            os.remove(filepath)
            
    return jsonify({'error': 'Please upload a valid .zip file.'}), 400

def parse_psobank_file(content):
    # Replace with actual parsing logic
    return {'type': 'psobank', 'content': content.decode('utf-8', errors='ignore')}

def parse_pso_char_file(content):
    # Replace with actual parsing logic
    return {'type': 'psochar', 'content': content.decode('utf-8', errors='ignore')}

if __name__ == '__main__':
    app.run(debug=True) 