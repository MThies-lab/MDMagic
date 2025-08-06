# Markdown Magic - Deployment Guide

## Overview

Markdown Magic can be deployed in three ways:
1. **Standalone Desktop App** (macOS/Windows/Linux)
2. **Streamlit Web App** (for local/cloud hosting)
3. **Flask Web App** (for website integration)

---

## 1. Standalone Desktop App

### Building for macOS

1. **Install py2app**:
   ```bash
   pip install py2app
   ```

2. **Build the app**:
   ```bash
   # Clean previous builds
   rm -rf build dist
   
   # Build the application
   python setup.py py2app
   ```

3. **Test the app**:
   ```bash
   open dist/Markdown\ Magic.app
   ```

4. **Create DMG for distribution**:
   ```bash
   # Install create-dmg
   brew install create-dmg
   
   # Create DMG
   create-dmg \
     --volname "Markdown Magic" \
     --window-pos 200 120 \
     --window-size 800 400 \
     --icon-size 100 \
     --icon "Markdown Magic.app" 200 190 \
     --app-drop-link 600 185 \
     "MarkdownMagic.dmg" \
     "dist/Markdown Magic.app"
   ```

### Building for Windows

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Create Windows executable**:
   ```bash
   pyinstaller --onedir --windowed --name "Markdown Magic" launch_markdown_magic.py
   ```

3. **Create installer** (optional):
   Use NSIS or Inno Setup to create a Windows installer.

---

## 2. Streamlit Web App

### Local Development

1. **Install Streamlit**:
   ```bash
   pip install streamlit
   ```

2. **Run locally**:
   ```bash
   streamlit run markdown_magic_streamlit.py
   ```

### Cloud Deployment (Streamlit Cloud)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Markdown Magic Streamlit app"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `markdown_magic_streamlit.py` as the main file
   - Deploy

### Self-hosted with Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "markdown_magic_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t markdown-magic-streamlit .
docker run -p 8501:8501 markdown-magic-streamlit
```

---

## 3. Flask Web App (Website Integration)

### Local Development

1. **Install Flask**:
   ```bash
   pip install flask gunicorn
   ```

2. **Run locally**:
   ```bash
   python markdown_magic_flask.py
   ```

### Production Deployment

#### Option A: Using Gunicorn

1. **Create `wsgi.py`**:
   ```python
   from markdown_magic_flask import app
   
   if __name__ == "__main__":
       app.run()
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:8000 wsgi:app
   ```

#### Option B: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "markdown_magic_flask:app"]
```

#### Option C: Integration with Existing Website

If you have an existing website, you can integrate the Flask app:

1. **As a subdirectory** (e.g., `yoursite.com/markdown-magic/`)
2. **As a subdomain** (e.g., `markdown-magic.yoursite.com`)
3. **Using reverse proxy** (Nginx/Apache)

**Nginx configuration example**:
```nginx
location /markdown-magic/ {
    proxy_pass http://127.0.0.1:5000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## Environment Setup

### Requirements Files

**For Standalone App** (`requirements_standalone.txt`):
```
PyQt5>=5.15.0
PyMuPDF>=1.18.0
python-docx>=0.8.10
openpyxl>=3.0.5
beautifulsoup4>=4.9.0
striprtf>=0.0.15
lxml>=4.6.0
Pillow>=8.0.0
pytesseract>=0.3.7
tqdm>=4.50.0
py2app>=0.28.0
```

**For Web Apps** (`requirements_web.txt`):
```
# Core dependencies
PyMuPDF>=1.18.0
python-docx>=0.8.10
openpyxl>=3.0.5
beautifulsoup4>=4.9.0
striprtf>=0.0.15
lxml>=4.6.0
Pillow>=8.0.0
pytesseract>=0.3.7
tqdm>=4.50.0

# Web frameworks
streamlit>=1.28.0
flask>=2.3.0
gunicorn>=21.0.0
```

### System Dependencies

**For OCR functionality**, install Tesseract:

- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **Windows**: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

---

## Security Considerations

### For Web Deployments

1. **File Upload Limits**:
   ```python
   app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
   ```

2. **Secure File Handling**:
   ```python
   from werkzeug.utils import secure_filename
   filename = secure_filename(file.filename)
   ```

3. **Temporary File Cleanup**:
   - Implement automatic cleanup of old files
   - Use session-based temporary directories
   - Set file retention policies

4. **Rate Limiting**:
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(
       app,
       key_func=lambda: request.remote_addr,
       default_limits=["100 per hour"]
   )
   ```

5. **HTTPS/SSL**:
   - Always use HTTPS in production
   - Configure proper SSL certificates

---

## Monitoring and Maintenance

### Logging

Add proper logging to track usage and errors:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('markdown_magic.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

Implement health check endpoints:

```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '1.0.0'
    })
```

### Performance Optimization

1. **Async Processing**: Use Celery for long-running conversions
2. **Caching**: Cache converted files for repeat requests
3. **Load Balancing**: Use multiple instances behind a load balancer

---

## Troubleshooting

### Common Issues

1. **Tesseract not found**:
   - Ensure Tesseract is installed and in PATH
   - Set `TESSDATA_PREFIX` environment variable

2. **Memory issues with large files**:
   - Implement file size limits
   - Process files in chunks
   - Use streaming for large uploads

3. **Permission errors**:
   - Ensure write permissions for temporary directories
   - Use proper user permissions in Docker

4. **Dependency conflicts**:
   - Use virtual environments
   - Pin dependency versions
   - Test in clean environments

### Logs to Monitor

- Conversion success/failure rates
- Processing times
- File sizes and types
- Error patterns
- Resource usage (CPU, memory, disk)

---

## Update and Maintenance

### Version Management

1. **Tag releases**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Update dependencies regularly**:
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

3. **Test before deployment**:
   - Unit tests for core functionality
   - Integration tests for web endpoints
   - Load testing for performance

### Backup and Recovery

- Regular backups of configuration
- Database backups (if using database)
- Disaster recovery procedures
- Rollback procedures for failed deployments