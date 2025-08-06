# ✨ Markdown Magic

Transform any document into beautiful Markdown with AI-powered conversion and intelligent image processing.

![Markdown Magic Banner](https://via.placeholder.com/800x200/667eea/ffffff?text=✨+Markdown+Magic)

## 🚀 Features

### 📄 **Multi-Format Support**
- **Documents**: PDF, Word (DOCX, DOC), RTF, TXT
- **Web**: HTML, HTM  
- **Spreadsheets**: Excel (XLSX, XLS)
- **Images**: PNG, JPEG, TIFF, BMP with OCR

### 🖼️ **Intelligent Image Processing**
- Automatic image extraction from documents
- OCR text recognition with multiple language support
- Smart alt-text generation
- PNG conversion with quality optimization

### 🔒 **Privacy First**
- **100% Local Processing** - No data leaves your machine
- **No Internet Required** - Works completely offline
- **Secure** - No external APIs or cloud services

### 🎯 **Multiple Deployment Options**
- **Standalone Desktop App** (macOS, Windows, Linux)
- **Web Interface** (Streamlit or Flask)
- **Website Integration** ready

## 📋 Quick Start

### Desktop App (Recommended for Personal Use)

1. **Download** the latest release for your platform
2. **Install** dependencies (see below)
3. **Launch** the application
4. **Drag & drop** files or use "Add Files"
5. **Select** output folder
6. **Convert** to Markdown! ✨

### Web Interface (For Website Integration)

```bash
# Clone the repository
git clone https://github.com/yourusername/markdown-magic.git
cd markdown-magic

# Install dependencies
pip install -r requirements.txt

# Run Streamlit version (user-friendly)
streamlit run markdown_magic_streamlit.py

# OR run Flask version (for website integration)
python markdown_magic_flask.py
```

## 🛠️ Installation

### System Requirements

- **Python 3.6+**
- **Operating System**: macOS, Windows, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 500MB free space

### Dependencies

#### Required Python Packages
```bash
pip install -r requirements.txt
```

#### System Dependencies (for OCR)

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**Windows:**
Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Automated Setup

For a guided installation experience:

```bash
python build_app.py
```

This script will:
- ✅ Check system requirements
- ✅ Install dependencies
- ✅ Build standalone apps
- ✅ Set up web deployments

## 🎨 Usage Examples

### Basic Conversion

```python
from document_converter import DocumentConverter

converter = DocumentConverter()
output_file = converter.convert_to_markdown("document.pdf", "output.md")
print(f"Converted to: {output_file}")
```

### Batch Processing

```python
from batch_processor import BatchProcessor
from document_converter import DocumentConverter

converter = DocumentConverter()
batch_processor = BatchProcessor()

files = ["doc1.pdf", "doc2.docx", "doc3.html"]
results = batch_processor.process_batch(files, "output_folder", converter)

print(f"Successfully converted: {len(results.successful_files)} files")
```

### Web API Usage

```bash
# Start the Flask web server
python markdown_magic_flask.py

# Upload and convert via HTTP POST
curl -X POST -F "files=@document.pdf" http://localhost:5000/convert
```

## 🏗️ Building from Source

### Desktop Applications

**macOS:**
```bash
python setup.py py2app
```

**Windows:**
```bash
pyinstaller --windowed launch_markdown_magic.py
```

**Linux:**
```bash
pyinstaller launch_markdown_magic.py
```

### Web Deployment

**Docker (Recommended):**
```bash
# Streamlit version
docker build -f Dockerfile.streamlit -t markdown-magic-web .
docker run -p 8501:8501 markdown-magic-web

# Flask version  
docker build -f Dockerfile.flask -t markdown-magic-api .
docker run -p 5000:5000 markdown-magic-api
```

**Manual:**
```bash
# For development
streamlit run markdown_magic_streamlit.py

# For production
gunicorn --bind 0.0.0.0:5000 markdown_magic_flask:app
```

## 🌐 Deployment Options

### 1. Personal Use
- **Desktop App**: Download and install the standalone application
- **Best for**: Individual users, offline processing

### 2. Website Integration
- **Flask Web App**: Integrate into existing websites
- **Streamlit App**: Quick deployment for teams
- **Best for**: Small teams, internal tools

### 3. Enterprise/Cloud
- **Docker Containers**: Scale with Kubernetes
- **API Integration**: RESTful API for custom applications
- **Best for**: High-volume processing, enterprise environments

## 📊 Supported Formats

| Input Format | Extension | Image Extraction | OCR Support | Notes |
|--------------|-----------|------------------|-------------|-------|
| PDF | `.pdf` | ✅ | ✅ | Full support with PyMuPDF |
| Word | `.docx`, `.doc` | ✅ | ✅ | Modern and legacy formats |
| RTF | `.rtf` | ✅ | ✅ | Rich Text Format |
| HTML | `.html`, `.htm` | ✅ | ✅ | Web pages |
| Excel | `.xlsx`, `.xls` | ⚠️ | ⚠️ | Tables converted to Markdown |
| Text | `.txt` | ❌ | ❌ | Plain text |
| Images | `.png`, `.jpg`, `.tiff`, `.bmp` | ✅ | ✅ | Direct OCR processing |

## ⚙️ Configuration

### OCR Settings

```python
# Configure OCR language
converter.configure_ocr(
    enabled=True,
    language='eng'  # English, 'spa' for Spanish, etc.
)
```

### Image Processing

```python
# Configure image processing
image_processor = ImageProcessor()
image_processor.set_quality(8)  # 1-10 scale
image_processor.enable_enhancement(True)
```

### Batch Processing Limits

```python
# Set batch processing limits
batch_processor = BatchProcessor(
    max_batch_size_mb=250,  # 250MB limit
    timeout_seconds=300     # 5 minute timeout
)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/markdown-magic.git
cd markdown-magic

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to all functions
- Write tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyMuPDF** for PDF processing
- **Tesseract OCR** for optical character recognition
- **PyQt5** for the desktop GUI
- **Streamlit** and **Flask** for web interfaces
- **All contributors** who helped improve this project

## 📞 Support

### Getting Help

- 📖 **Documentation**: Check our [Wiki](https://github.com/yourusername/markdown-magic/wiki)
- 🐛 **Bug Reports**: [Create an issue](https://github.com/yourusername/markdown-magic/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/markdown-magic/discussions)
- 📧 **Email**: support@markdownmagic.com

### FAQ

**Q: Why isn't OCR working?**
A: Make sure Tesseract is installed and in your system PATH.

**Q: Can I process password-protected PDFs?**
A: Currently not supported. Please remove password protection first.

**Q: What's the maximum file size?**
A: Default limit is 250MB total per batch. This can be configured.

**Q: Does this work offline?**
A: Yes! Markdown Magic works completely offline with no internet required.

## 🗺️ Roadmap

### Version 1.1 (Coming Soon)
- [ ] Password-protected PDF support
- [ ] PowerPoint (PPTX) conversion
- [ ] Advanced table formatting
- [ ] Custom output templates

### Version 1.2 (Future)
- [ ] Real-time collaboration features
- [ ] Cloud storage integration
- [ ] Advanced OCR with AI enhancement
- [ ] Mobile app versions

### Version 2.0 (Vision)
- [ ] AI-powered content understanding
- [ ] Automated content summarization
- [ ] Multi-language translation
- [ ] Enterprise features

---

<div align="center">

**Made with ❤️ by the Markdown Magic Team**

⭐ **Star this repo** if you find it helpful!

[Website](https://markdownmagic.com) • [Documentation](https://docs.markdownmagic.com) • [Support](mailto:support@markdownmagic.com)

</div>