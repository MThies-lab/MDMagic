#!/usr/bin/env python3
"""
Markdown Magic - Flask Web Application
Web interface for document conversion that can be hosted on your website
"""

from flask import Flask, request, render_template_string, send_file, jsonify, redirect, url_for
import tempfile
import os
import zipfile
import io
from pathlib import Path
import uuid
from werkzeug.utils import secure_filename
from document_converter import DocumentConverter
from batch_processor import BatchProcessor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.secret_key = 'markdown_magic_secret_key_change_in_production'

# Store conversion results temporarily
conversion_results = {}

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✨ Markdown Magic</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 40px 20px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .upload-section {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            background: #f8f9ff;
            transition: all 0.3s ease;
        }
        
        .upload-section:hover {
            background: #f0f2ff;
            border-color: #764ba2;
        }
        
        .upload-section.dragover {
            background: #e8ecff;
            border-color: #5a67d8;
            transform: scale(1.02);
        }
        
        .file-input {
            display: none;
        }
        
        .upload-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
        }
        
        .upload-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .settings {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .settings h3 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .setting-group {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .setting-item {
            flex: 1;
            min-width: 200px;
        }
        
        .setting-item label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }
        
        .setting-item input,
        .setting-item select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        
        .setting-item input:focus,
        .setting-item select:focus {
            border-color: #667eea;
            outline: none;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .checkbox-item input[type="checkbox"] {
            width: auto;
        }
        
        .file-list {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
        }
        
        .file-item {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .file-info {
            flex: 1;
        }
        
        .file-name {
            font-weight: 600;
            color: #333;
        }
        
        .file-size {
            color: #666;
            font-size: 0.9em;
        }
        
        .remove-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8em;
        }
        
        .convert-btn {
            background: linear-gradient(135deg, #2ed573 0%, #17a2b8 100%);
            color: white;
            border: none;
            padding: 20px 40px;
            border-radius: 25px;
            font-size: 1.2em;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .convert-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(46, 213, 115, 0.3);
        }
        
        .convert-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .progress {
            background: #e9ecef;
            border-radius: 25px;
            height: 30px;
            margin-bottom: 20px;
            overflow: hidden;
            display: none;
        }
        
        .progress-bar {
            background: linear-gradient(135deg, #2ed573 0%, #17a2b8 100%);
            height: 100%;
            border-radius: 25px;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        
        .results {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
            display: none;
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .download-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .download-btn {
            background: #007bff;
            color: white;
            text-decoration: none;
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s ease;
            display: block;
        }
        
        .download-btn:hover {
            background: #0056b3;
            text-decoration: none;
            color: white;
            transform: translateY(-2px);
        }
        
        .download-all {
            background: #28a745;
            grid-column: 1 / -1;
            font-size: 1.1em;
            font-weight: 600;
        }
        
        .download-all:hover {
            background: #1e7e34;
        }
        
        .supported-formats {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
        }
        
        .format-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .format-category {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .format-category h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        
        .format-list {
            list-style: none;
        }
        
        .format-list li {
            padding: 5px 0;
            color: #666;
        }
        
        .format-list li:before {
            content: "• ";
            color: #667eea;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .content {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .setting-group {
                flex-direction: column;
            }
            
            .setting-item {
                min-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ Markdown Magic</h1>
            <p>Transform any document into beautiful Markdown with AI-powered conversion</p>
        </div>
        
        <div class="content">
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-section" id="uploadSection">
                    <h3>📁 Upload Documents</h3>
                    <p>Drag and drop files here or click to browse</p>
                    <input type="file" id="fileInput" name="files" multiple 
                           accept=".pdf,.docx,.doc,.rtf,.txt,.html,.htm,.xlsx,.xls,.png,.jpg,.jpeg,.tiff,.bmp"
                           class="file-input">
                    <button type="button" class="upload-btn" onclick="document.getElementById('fileInput').click()">
                        📂 Choose Files
                    </button>
                </div>
                
                <div class="file-list" id="fileList" style="display: none;">
                    <h3>📋 Selected Files</h3>
                    <div id="fileItems"></div>
                </div>
                
                <div class="settings">
                    <h3>⚙️ Conversion Settings</h3>
                    
                    <div class="setting-group">
                        <div class="setting-item checkbox-item">
                            <input type="checkbox" id="enableOcr" name="enable_ocr" checked>
                            <label for="enableOcr">Enable OCR for images</label>
                        </div>
                        
                        <div class="setting-item">
                            <label for="ocrLanguage">OCR Language</label>
                            <select id="ocrLanguage" name="ocr_language">
                                <option value="eng">English</option>
                                <option value="spa">Spanish</option>
                                <option value="fra">French</option>
                                <option value="deu">German</option>
                                <option value="ita">Italian</option>
                                <option value="por">Portuguese</option>
                                <option value="rus">Russian</option>
                                <option value="chi_sim">Chinese (Simplified)</option>
                                <option value="jpn">Japanese</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="setting-group">
                        <div class="setting-item checkbox-item">
                            <input type="checkbox" id="extractImages" name="extract_images" checked>
                            <label for="extractImages">Extract and process images</label>
                        </div>
                        
                        <div class="setting-item checkbox-item">
                            <input type="checkbox" id="preserveFormatting" name="preserve_formatting" checked>
                            <label for="preserveFormatting">Preserve original formatting</label>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="convert-btn" id="convertBtn" disabled>
                    ✨ Convert to Markdown
                </button>
                
                <div class="progress" id="progress">
                    <div class="progress-bar" id="progressBar">0%</div>
                </div>
            </form>
            
            <div class="results" id="results"></div>
            
            <div class="supported-formats">
                <h3>🎯 Supported Formats</h3>
                <div class="format-grid">
                    <div class="format-category">
                        <h4>📄 Documents</h4>
                        <ul class="format-list">
                            <li>PDF</li>
                            <li>Word (DOCX, DOC)</li>
                            <li>Rich Text (RTF)</li>
                            <li>Plain Text (TXT)</li>
                        </ul>
                    </div>
                    
                    <div class="format-category">
                        <h4>🌐 Web</h4>
                        <ul class="format-list">
                            <li>HTML</li>
                            <li>HTM</li>
                        </ul>
                    </div>
                    
                    <div class="format-category">
                        <h4>📊 Spreadsheets</h4>
                        <ul class="format-list">
                            <li>Excel (XLSX, XLS)</li>
                        </ul>
                    </div>
                    
                    <div class="format-category">
                        <h4>🖼️ Images</h4>
                        <ul class="format-list">
                            <li>PNG</li>
                            <li>JPEG</li>
                            <li>TIFF</li>
                            <li>BMP</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        
        // File input handling
        document.getElementById('fileInput').addEventListener('change', handleFileSelect);
        
        // Drag and drop handling
        const uploadSection = document.getElementById('uploadSection');
        
        uploadSection.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadSection.classList.add('dragover');
        });
        
        uploadSection.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadSection.classList.remove('dragover');
        });
        
        uploadSection.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadSection.classList.remove('dragover');
            const files = Array.from(e.dataTransfer.files);
            handleFiles(files);
        });
        
        function handleFileSelect(e) {
            const files = Array.from(e.target.files);
            handleFiles(files);
        }
        
        function handleFiles(files) {
            files.forEach(file => {
                if (!selectedFiles.find(f => f.name === file.name && f.size === file.size)) {
                    selectedFiles.push(file);
                }
            });
            updateFileList();
            updateConvertButton();
        }
        
        function removeFile(index) {
            selectedFiles.splice(index, 1);
            updateFileList();
            updateConvertButton();
        }
        
        function updateFileList() {
            const fileList = document.getElementById('fileList');
            const fileItems = document.getElementById('fileItems');
            
            if (selectedFiles.length === 0) {
                fileList.style.display = 'none';
                return;
            }
            
            fileList.style.display = 'block';
            fileItems.innerHTML = '';
            
            selectedFiles.forEach((file, index) => {
                const fileSize = (file.size / 1024 / 1024).toFixed(2);
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <div class="file-info">
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${fileSize} MB</div>
                    </div>
                    <button type="button" class="remove-btn" onclick="removeFile(${index})">Remove</button>
                `;
                fileItems.appendChild(fileItem);
            });
        }
        
        function updateConvertButton() {
            const convertBtn = document.getElementById('convertBtn');
            convertBtn.disabled = selectedFiles.length === 0;
        }
        
        // Form submission
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (selectedFiles.length === 0) {
                alert('Please select files to convert');
                return;
            }
            
            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files', file);
            });
            
            // Add settings
            formData.append('enable_ocr', document.getElementById('enableOcr').checked);
            formData.append('ocr_language', document.getElementById('ocrLanguage').value);
            formData.append('extract_images', document.getElementById('extractImages').checked);
            formData.append('preserve_formatting', document.getElementById('preserveFormatting').checked);
            
            // Show progress
            const convertBtn = document.getElementById('convertBtn');
            const progress = document.getElementById('progress');
            const results = document.getElementById('results');
            
            convertBtn.disabled = true;
            convertBtn.textContent = '🔄 Converting...';
            progress.style.display = 'block';
            results.style.display = 'none';
            
            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const result = await response.json();
                    showResults(result);
                } else {
                    const error = await response.text();
                    showError('Conversion failed: ' + error);
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
            
            // Reset UI
            convertBtn.disabled = false;
            convertBtn.textContent = '✨ Convert to Markdown';
            progress.style.display = 'none';
        });
        
        function showResults(result) {
            const results = document.getElementById('results');
            results.style.display = 'block';
            
            let html = '';
            
            if (result.successful_files && result.successful_files.length > 0) {
                html += `
                    <div class="success">
                        <h3>✅ Conversion Successful!</h3>
                        <p>${result.successful_files.length} file(s) converted successfully</p>
                    </div>
                    
                    <div class="download-section">
                        <a href="/download_all/${result.session_id}" class="download-btn download-all">
                            📦 Download All Files (ZIP)
                        </a>
                `;
                
                result.successful_files.forEach(file => {
                    const filename = file.split('/').pop();
                    html += `
                        <a href="/download/${result.session_id}/${encodeURIComponent(filename)}" class="download-btn">
                            📄 ${filename}
                        </a>
                    `;
                });
                
                html += '</div>';
            }
            
            if (result.failed_files && result.failed_files.length > 0) {
                html += '<div class="error"><h3>⚠️ Some Files Failed</h3><ul>';
                result.failed_files.forEach(([filename, error]) => {
                    html += `<li>${filename}: ${error}</li>`;
                });
                html += '</ul></div>';
            }
            
            results.innerHTML = html;
        }
        
        function showError(message) {
            const results = document.getElementById('results');
            results.style.display = 'block';
            results.innerHTML = `
                <div class="error">
                    <h3>❌ Error</h3>
                    <p>${message}</p>
                </div>
            `;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/convert', methods=['POST'])
def convert_files():
    """Handle file conversion"""
    try:
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({'error': 'No files provided'}), 400
        
        # Get settings
        settings = {
            'enable_ocr': request.form.get('enable_ocr') == 'true',
            'ocr_language': request.form.get('ocr_language', 'eng'),
            'extract_images': request.form.get('extract_images') == 'true',
            'preserve_formatting': request.form.get('preserve_formatting') == 'true'
        }
        
        # Create temporary directories
        session_id = str(uuid.uuid4())
        temp_input_dir = tempfile.mkdtemp(prefix=f'markdown_magic_input_{session_id}_')
        temp_output_dir = tempfile.mkdtemp(prefix=f'markdown_magic_output_{session_id}_')
        
        # Save uploaded files
        input_files = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(temp_input_dir, filename)
                file.save(file_path)
                input_files.append(file_path)
        
        # Initialize converter and batch processor
        converter = DocumentConverter()
        batch_processor = BatchProcessor()
        
        # Configure converter with settings
        if hasattr(converter, 'configure_ocr'):
            converter.configure_ocr(
                enabled=settings['enable_ocr'],
                language=settings['ocr_language']
            )
        
        # Process files
        results = batch_processor.process_batch(
            input_files,
            temp_output_dir,
            converter
        )
        
        # Store results for download
        conversion_results[session_id] = {
            'input_dir': temp_input_dir,
            'output_dir': temp_output_dir,
            'results': results,
            'timestamp': time.time()
        }
        
        # Clean old results (older than 1 hour)
        cleanup_old_results()
        
        return jsonify({
            'session_id': session_id,
            'successful_files': [os.path.basename(f) for f in results.successful_files],
            'failed_files': results.failed_files,
            'total_files': results.total_files
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Download individual converted file"""
    if session_id not in conversion_results:
        return "Session not found", 404
    
    result_data = conversion_results[session_id]
    file_path = os.path.join(result_data['output_dir'], filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404
    
    return send_file(file_path, as_attachment=True, download_name=filename)

@app.route('/download_all/<session_id>')
def download_all(session_id):
    """Download all converted files as ZIP"""
    if session_id not in conversion_results:
        return "Session not found", 404
    
    result_data = conversion_results[session_id]
    results = result_data['results']
    
    # Create ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in results.successful_files:
            filename = os.path.basename(file_path)
            zip_file.write(file_path, filename)
    
    zip_buffer.seek(0)
    
    return send_file(
        io.BytesIO(zip_buffer.getvalue()),
        mimetype='application/zip',
        as_attachment=True,
        download_name='markdown_magic_conversion.zip'
    )

def cleanup_old_results():
    """Clean up old conversion results"""
    import time
    current_time = time.time()
    sessions_to_remove = []
    
    for session_id, data in conversion_results.items():
        # Remove sessions older than 1 hour
        if current_time - data['timestamp'] > 3600:
            sessions_to_remove.append(session_id)
            
            # Clean up temporary directories
            try:
                import shutil
                if os.path.exists(data['input_dir']):
                    shutil.rmtree(data['input_dir'])
                if os.path.exists(data['output_dir']):
                    shutil.rmtree(data['output_dir'])
            except Exception as e:
                print(f"Error cleaning up session {session_id}: {e}")
    
    for session_id in sessions_to_remove:
        del conversion_results[session_id]

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Markdown Magic'})

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For production (with gunicorn, etc.)
    pass