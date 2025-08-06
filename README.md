# 🚀 Markdown Magic

**The Ultimate Document-to-Markdown Conversion Suite with AI-Powered Image Descriptions**

Transform any document into beautiful, structured Markdown with advanced batch processing, OCR capabilities, AI-enhanced image descriptions, and intelligent format preservation.

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![AI](https://img.shields.io/badge/AI-Enhanced-purple)

---

## 📋 What is Markdown Magic?

Markdown Magic is a comprehensive document conversion toolkit that transforms various file formats into clean, structured Markdown. It features both a desktop GUI application and a web-based interface, designed for researchers, writers, developers, and content creators who need reliable document conversion.

### **🆕 What's New: AI-Enhanced Image Processing**

Your Markdown Magic now features **AI-Powered Image Descriptions** that go beyond basic OCR:

#### **Before (OCR Only):**
```markdown
![Image (1), page 2, Image content:](images/image_1.jpg)
```

#### **After (AI + OCR):**
```markdown
![Image 1, page 2, a red sports car parked in front of a modern building, Text: "FERRARI 458"](images/image_1.jpg)
```

## 🎯 Purpose & Mission

**Convert Everything to Markdown, Effortlessly.**

- Transform legacy documents into modern, portable Markdown format
- Preserve document structure, formatting, and embedded content
- Enable batch processing for large document collections
- Provide OCR capabilities for scanned documents and images
- Generate AI-powered descriptions for visual content
- Offer both desktop and web-based conversion interfaces

## 🔥 Key Capabilities

### 📄 **Supported File Formats**
- **Text Documents:** `.txt`, `.rtf`
- **Microsoft Office:** `.docx`, `.doc`, `.xlsx`, `.xls`
- **PDF Documents:** `.pdf` (with OCR support)
- **Web Documents:** `.html`, `.htm`
- **Images:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.tif`
- **OpenDocument:** `.odt`

### ⚡ **Advanced Features**
- **Batch Processing:** Convert hundreds of files simultaneously
- **OCR Text Recognition:** Extract text from images and scanned PDFs
- **🤖 AI Image Descriptions:** Generate meaningful visual content descriptions
- **Multi-language OCR:** Support for 11+ languages including English, Spanish, French, German, Chinese, Japanese, Korean, Arabic
- **Smart Structure Detection:** Automatically identify headings, lists, tables, and formatting
- **Image Extraction:** Save embedded images with proper linking
- **Format Preservation:** Maintain original document structure and styling
- **Progress Tracking:** Real-time conversion progress with detailed status
- **Error Handling:** Robust error recovery and detailed reporting
- **Size Validation:** Intelligent file size limits (250MB batch limit)
- **Hybrid Processing:** Combines OCR text extraction with AI visual analysis

### 🖥️ **Multiple Interfaces**
- **Desktop GUI:** Native cross-platform application with drag-and-drop
- **Web Interface:** Browser-based converter with modern UI
- **Command Line:** Scriptable automation support

## 🥊 Advantages Over MCP "Markitdown"

| Feature | Markdown Magic | MCP Markitdown |
|---------|----------------|----------------|
| **Batch Processing** | ✅ Advanced batch with progress tracking | ❌ Single file only |
| **OCR Support** | ✅ Multi-language OCR with Tesseract | ❌ No OCR capabilities |
| **🤖 AI Image Descriptions** | ✅ AI-powered visual content analysis | ❌ No AI capabilities |
| **GUI Interface** | ✅ Full desktop + web interface | ❌ Command line only |
| **Image Extraction** | ✅ Automatic image extraction/linking | ❌ Limited image support |
| **Format Preservation** | ✅ Intelligent structure detection | ❌ Basic conversion |
| **Error Recovery** | ✅ Robust error handling + retry | ❌ Basic error handling |
| **Progress Tracking** | ✅ Real-time progress with ETA | ❌ No progress indication |
| **File Size Limits** | ✅ Smart validation (250MB batches) | ❌ No size management |
| **Web Interface** | ✅ Modern web app with drag-drop | ❌ No web interface |
| **Multi-platform** | ✅ Windows, macOS, Linux + Web | ❌ Platform dependent |
| **Settings Control** | ✅ Granular conversion settings | ❌ Limited customization |
| **Smart Alt-Text** | ✅ AI-generated meaningful descriptions | ❌ No alt-text generation |

---

## 📋 System Requirements

### **Python Version**
- **Required:** Python 3.8 or higher
- **Recommended:** Python 3.9 - 3.12
- **Tested:** Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

### **Operating Systems**
- **Windows:** 10, 11 (64-bit)
- **macOS:** 10.14+ (Mojave and newer)
- **Linux:** Ubuntu 18.04+, CentOS 7+, Debian 9+

### **Hardware Requirements**
- **RAM:** 4GB minimum, 8GB+ recommended (with AI features)
- **Storage:** 500MB free space + 1-2GB additional for AI models (optional)
- **Processor:** Any modern CPU (GPU optional but faster for AI processing)

---

## 📦 Required Python Libraries

### **Core Dependencies**
```
PyQt5>=5.15.0          # Desktop GUI framework
Pillow>=8.0.0           # Image processing
pytesseract>=0.3.7      # OCR text recognition
PyMuPDF>=1.18.0         # PDF processing
python-docx>=0.8.10     # Word document processing
beautifulsoup4>=4.9.0   # HTML parsing
striprtf>=0.0.15        # RTF document processing
openpyxl>=3.0.5         # Excel file processing
lxml>=4.6.0             # XML processing
tqdm>=4.60.0            # Progress bars
```

### **Development Dependencies**
```
py2app>=0.28.0          # macOS app packaging (macOS only)
```

### **🤖 AI Vision Dependencies (Optional - Enhanced Features)**
```
transformers>=4.35.0    # AI model framework
torch>=2.0.0           # Deep learning library
torchvision>=0.15.0    # Computer vision library
```

---

## 🛠️ Installation Guide

### **Step 1: Check Your Python Installation**

First, let's verify you have Python installed:

**On Windows:**
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. In the black window that opens, type: `python3 --version`
4. Press Enter

**On macOS:**
1. Press `Cmd + Space`
2. Type `terminal` and press Enter
3. In the terminal window, type: `python3 --version`
4. Press Enter

**On Linux:**
1. Press `Ctrl + Alt + T`
2. Type: `python3 --version`
3. Press Enter

**Expected Result:** You should see something like `Python 3.9.7` or similar. If you see an error, you need to install Python first.

---

### **Step 2: Install Python (If Needed)**

**If Python is not installed:**

**Windows:**
1. Go to https://python.org/downloads
2. Click "Download Python" (latest version)
3. Run the downloaded file
4. ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation
5. Click "Install Now"

**macOS:**
1. Go to https://python.org/downloads
2. Download the latest Python version
3. Run the installer and follow prompts

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

### **Step 3: Install Tesseract OCR (For Text Recognition)**

**Windows:**
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Remember the installation path (usually `C:\Program Files\Tesseract-OCR\`)

**macOS:**
1. Install Homebrew if you don't have it: https://brew.sh
2. Open Terminal and run:
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install tesseract-ocr
```

---

### **Step 4: Download Markdown Magic**

**Option A: Download ZIP**
1. Go to: https://github.com/MThies-lab/Markdown-Magic
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your desired location (like Desktop)

**Option B: Using Git (Advanced)**
```bash
git clone https://github.com/MThies-lab/Markdown-Magic.git
cd Markdown-Magic
```

---

### **Step 5: Open Terminal/Command Prompt in Project Folder**

**Windows:**
1. Open File Explorer
2. Navigate to your Markdown-Magic folder
3. Hold `Shift` and right-click in the folder
4. Select "Open PowerShell window here" or "Open command window here"

**macOS:**
1. Open Finder
2. Navigate to your Markdown-Magic folder
3. Right-click the folder
4. Select "Services" → "New Terminal at Folder"

**Linux:**
1. Open your file manager
2. Navigate to the Markdown-Magic folder
3. Right-click and select "Open in Terminal"

---

### **Step 6: Create a Virtual Environment (Recommended)**

This keeps your project dependencies separate from other Python projects:

**Run these commands one at a time:**

**Windows:**
```cmd
python3 -m venv markdown_magic_env
markdown_magic_env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv markdown_magic_env
source markdown_magic_env/bin/activate
```

**You should see `(markdown_magic_env)` at the beginning of your command line.**

---

### **Step 7: Install Core Libraries**

**Run this single command:**

**Windows:**
```cmd
pip3 install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

**This will install all core dependencies. AI features are installed separately in the next section.**

---

## 🤖 AI Vision Setup (Optional Enhanced Features)

### **Step 8A: Install AI Dependencies (Optional)**

For AI-powered image descriptions, install additional libraries:

**Basic AI Installation:**
```bash
pip3 install transformers torch torchvision
```

**For Apple Silicon Macs (M1/M2/M3) - CPU Only:**
```bash
pip3 install transformers torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**For NVIDIA GPU Support (Optional - Much Faster):**
```bash
pip3 install transformers torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### **Step 8B: Test AI Installation**

```bash
python3 test_ai_vision.py
```

**Expected Output with AI:**
```
✅ AI Vision Processor: Available
✅ Enhanced Image Processor: Available  
✅ AI-Enhanced Document Converter: Available
🤖 AI Vision Models: ✅
```

**If AI libraries are not installed:**
```
❌ AI Vision components not available
🔄 Falling back to basic OCR-only processing...
```

### **AI Configuration Options**

```python
# Enable AI features (default if libraries installed)
converter = DocumentConverter(enable_ai=True)

# Disable AI for faster processing
converter = DocumentConverter(enable_ai=False)

# Custom settings
from ai_vision_processor import AIVisionProcessor
processor = AIVisionProcessor(
    enable_ai=True,
    ai_model_size='base'  # or 'large' for better quality
)
```

---

### **Step 9: Test Your Installation**

**Run the desktop application:**

**Windows:**
```cmd
python3 markdown_magic_gui.py
```

**macOS/Linux:**
```bash
python3 markdown_magic_gui.py
```

**Expected Result:** A green-themed desktop application should open with "MARKDOWN MAGIC" title.

---

### **Step 10: Test With a Sample File**

1. Create a simple text file on your desktop called `test.txt`
2. Add some text to it: "Hello world! This is a test."
3. Save the file
4. In Markdown Magic, click "ADD FILES"
5. Select your `test.txt` file
6. Click "OUTPUT FOLDER" and choose your Desktop
7. Click "CONVERT"
8. You should see a new file `test.md` created on your Desktop

**For AI Testing:**
- Try converting an image file (`.jpg`, `.png`)
- The generated markdown will include AI-generated descriptions if AI is enabled

---

## 🚀 Quick Start Guide

### **Desktop Application**
1. Run `python3 markdown_magic_gui.py`
2. Click "ADD FILES" or drag files into the window
3. Select output folder
4. Configure OCR settings if needed  
5. Enable/disable AI features in settings
6. Click "CONVERT"
7. Download converted files

### **Web Interface**
1. Set up the Wix web interface using the provided `wix_enhanced_widget.js`
2. Upload files through the web interface
3. Configure conversion settings
4. Process files and download results

### **Command Line Usage**
```python
from document_converter import DocumentConverter

# Basic conversion
converter = DocumentConverter()
result = converter.convert_to_markdown('my_document.pdf')

# With AI features
converter = DocumentConverter(enable_ai=True)
result = converter.convert_to_markdown('document_with_images.pdf')

# OCR only (faster)
converter = DocumentConverter(enable_ai=False)
result = converter.convert_to_markdown('text_document.pdf')
```

---

## 💡 AI Processing Examples

### **Hybrid Processing System:**

1. **Text Detection (OCR):** Tesseract extracts any readable text
2. **Visual Analysis (AI):** BLIP model generates image descriptions  
3. **Smart Combination:** Creates intelligent alt-text combining both

### **Example Processing Pipeline:**

**Input:** Screenshot of a data chart  
**OCR Result:** "Sales Q4 2023: $2.3M Revenue"  
**AI Result:** "a bar chart showing quarterly sales data"  
**Final Alt-Text:** `"Image 1, page 3, a bar chart showing quarterly sales data, Text: Sales Q4 2023: $2.3M Revenue"`

### **Code Examples:**

**1. Basic AI-enhanced image processing:**
```python
from ai_vision_processor import AIVisionProcessor

# Create processor with AI enabled
processor = AIVisionProcessor(enable_ai=True)

# Process an image file
output_md = processor.process_image_file('my_image.jpg')
print(f"Generated: {output_md}")
```

**2. Document conversion with AI:**
```python
from document_converter import DocumentConverter

# Create converter with AI features
converter = DocumentConverter(enable_ai=True)

# Convert a PDF with images
output_md = converter.convert_to_markdown('document.pdf')
print(f"Converted with AI descriptions: {output_md}")
```

**3. Disable AI for faster processing:**
```python
# For faster processing without AI descriptions
converter = DocumentConverter(enable_ai=False)
processor = ImageProcessor(enable_ai=False)
```

---

## 📈 Performance Comparison

| Feature | Basic OCR | AI + OCR |
|---------|-----------|-----------|
| Text Recognition | ✅ | ✅ |
| Image Descriptions | ❌ | ✅ |
| Meaningful Alt-Text | ❌ | ✅ |
| Processing Speed | ~1s/image | ~3s/image |
| Memory Usage | ~100MB | ~2GB |
| Offline Operation | ✅ | ✅ |
| Model Download | None | ~1GB first time |
| Setup Complexity | Simple | Moderate |
| Accuracy | High for text | High for text + visuals |

---

## 📞 Support & Troubleshooting

### **Common Issues**

**"Command not found" error:**
- Make sure Python is installed and added to PATH
- Try `python3` instead of `python` on macOS/Linux

**"Permission denied" errors:**
- Run terminal as administrator (Windows)
- Use `sudo` for system installations (Linux/macOS)

**Tesseract OCR not working:**
- Verify Tesseract installation path
- Check that Tesseract is in your system PATH

**GUI doesn't open:**
- Ensure PyQt5 is properly installed
- Try: `pip3 install --upgrade PyQt5`

**AI Features Not Working:**
- Check if AI libraries are installed: `pip3 list | grep transformers`
- Verify you have enough RAM (8GB+ recommended)
- First run downloads models (~1GB) - be patient

**"transformers not installed" Error:**
```bash
pip3 install transformers torch torchvision
```

**"CUDA out of memory" (GPU users):**
```python
# Force CPU usage
processor = AIVisionProcessor(enable_ai=True, force_cpu=True)
```

**Slow first-time AI processing:**
- AI models download automatically (~500MB-1GB)
- Subsequent runs are much faster
- Models are cached locally

**Import errors with AI:**
```python
# Check what's available
from ai_vision_processor import AIVisionProcessor
processor = AIVisionProcessor()
caps = processor.get_capabilities()
print(caps)  # Shows what features are working
```

### **Testing Your Setup**

**Test Core Features:**
```bash
python3 markdown_magic_gui.py
```

**Test AI Features:**
```bash
python3 test_ai_vision.py
```

**Test with Sample Image:**
```python
from ai_vision_processor import AIVisionProcessor

processor = AIVisionProcessor(enable_ai=True)
output_file = processor.process_image_file('test_image.jpg')
print(f"Generated: {output_file}")
```

### **Performance Optimization**

1. **First Run:** Let AI models download completely before batch processing
2. **Memory:** Close other applications when processing many large images
3. **Speed:** Use `enable_ai=False` for text-only documents
4. **Quality:** Use `ai_model_size='large'` for better descriptions of complex images
5. **Batch:** Process similar images together for better efficiency

### **Getting Help**
- 📧 Create an issue on GitHub
- 📖 Check the documentation in the `docs/` folder
- 🤝 Contribute improvements via pull requests
- 🧪 Run test scripts to diagnose issues

---

## 🔄 Migration from Basic Version

**No Breaking Changes!** Your existing code continues to work:

```python
# This still works exactly the same
from document_converter import DocumentConverter
converter = DocumentConverter()  # AI enabled by default if libraries installed

# Explicitly disable AI if needed
converter = DocumentConverter(enable_ai=False)
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Tesseract OCR** - For optical character recognition
- **PyQt5** - For the desktop GUI framework
- **PyMuPDF** - For PDF processing capabilities
- **Salesforce BLIP** - For AI-powered image descriptions
- **Transformers Library** - For state-of-the-art AI models
- **All contributors** - For making this project better

---

## 🌟 What You Get

### **Enhanced Alt-Text:**
- **Before:** `"Image (1), OCR not available"`
- **After:** `"Image 1, a person typing on a laptop computer"`

### **Comprehensive Analysis:**
```markdown
## AI Description
**Visual Content:** a red car parked in front of a building

## Extracted Text (OCR)
```
License: ABC-123
Model: Tesla Model 3
```

### **Better Accessibility:**
- Screen readers get meaningful descriptions
- Search engines can index visual content
- Content creators get automated image descriptions

---

**Made with ❤️ for the open source community**

*Transform your documents. Generate intelligent descriptions. Embrace the power of AI-enhanced Markdown conversion.* ✨

🎊 **Your Markdown Magic is now AI-powered!** 🎊