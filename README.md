# 🚀 Markdown Magic

**The Ultimate Document-to-Markdown Conversion Suite**

Transform any document into beautiful, structured Markdown with advanced batch processing, OCR capabilities, and intelligent format preservation.

Note: This project was created out of curiosity and necessity. If you find something that's broken, or could be better, please let me know! I built this either before the Markitdown MCP was live or before I knew about it. 

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📋 What is Markdown Magic?

Markdown Magic is a comprehensive local document conversion program that transforms various file formats into clean, structured Markdown. It follows the official Markdown Guide style guide by Matt Cone and features both a desktop GUI application designed for researchers, writers, developers, and content creators who need reliable document conversion.

## 🔥 Key Capabilities

Markdown Magic Transforms documents into modern, portable Markdown format for any use case, and preserves document structure, formatting, and embedded content. This program removes images from documents and places them in a separate cloned name folder, renaming the images in the order of their placement in the document. In the new markdown file, a placeholder for each image is generated in its place, clearly identifying which images belongs there. Additionally, the Tesseract OCR feature "reads" the image image to generate a brief description of each image it scans, and is part of the image placeholder. 

This program supports drag and drop and standard file upload, as well as batch processing up to 250 mb. This program is completely free, completely local and only has access to the folder the user designates to send the converted file to. 

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
- **Multi-language OCR:** Support for 11+ languages including English, Spanish, French, German, Chinese, Japanese, Korean, Arabic
- **Smart Structure Detection:** Automatically identify headings, lists, tables, and formatting
- **Image Extraction:** Save embedded images with proper linking
- **Format Preservation:** Maintain original document structure and styling
- **Progress Tracking:** Real-time conversion progress with detailed status
- **Error Handling:** Robust error recovery and detailed reporting
- **Size Validation:** Intelligent file size limits (250MB batch limit)

### 🖥️ **Multiple Interfaces**
- **Desktop GUI:** Native cross-platform application with drag-and-drop
- **Command Line:** Scriptable automation support

## 🥊 Advantages Over MCP "Markitdown"

| Feature | Markdown Magic | MCP Markitdown |
|---------|----------------|----------------|
| **Batch Processing** | ✅ Advanced batch with progress tracking | ❌ Single file only |
| **OCR Support** | ✅ Multi-language OCR with Tesseract | ❌ No OCR capabilities |
| **GUI Interface** | ✅ Full desktop interface | ❌ Command line only |
| **Image Extraction** | ✅ Automatic image extraction/linking | ❌ Limited image support |
| **Format Preservation** | ✅ Intelligent structure detection | ❌ Basic conversion |
| **Error Recovery** | ✅ Robust error handling + retry | ❌ Basic error handling |
| **Progress Tracking** | ✅ Real-time progress with ETA | ❌ No progress indication |
| **File Size Limits** | ✅ Smart validation (250MB batches) | ❌ No size management |
| **Web Interface** | ✅ Modern web app with drag-drop | ❌ No web interface |
| **Multi-platform** | ✅ Windows, macOS, Linux  | ❌ Platform dependent |
| **Settings Control** | ✅ Granular conversion settings | ❌ Limited customization |

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
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 500MB free space
- **Processor:** Any modern CPU (OCR benefits from multi-core)

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

---

## 🛠️ Installation Guide

### **Step 1: Check Your Python Installation**

First, let's verify you have Python installed:

**On Windows:**
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. In the black window that opens, type: `python --version`
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
python -m venv markdown_magic_env
markdown_magic_env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv markdown_magic_env
source markdown_magic_env/bin/activate
```

**You should see `(markdown_magic_env)` at the beginning of your command line.**

---

### **Step 7: Install Required Libraries**

**Run this single command:**

**Windows:**
```cmd
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

**This will take 2-5 minutes to download and install everything.**

---

### **Step 8: Test Your Installation**

**Run the desktop application:**

**Windows:**
```cmd
python markdown_magic_gui.py
```

**macOS/Linux:**
```bash
python3 markdown_magic_gui.py
```

**Expected Result:** A green-themed desktop application should open with "MARKDOWN MAGIC" title.

---

### **Step 9: Test With a Sample File**

1. Create a simple text file on your desktop called `test.txt`
2. Add some text to it: "Hello world! This is a test."
3. Save the file
4. In Markdown Magic, click "ADD FILES"
5. Select your `test.txt` file
6. Click "OUTPUT FOLDER" and choose your Desktop
7. Click "CONVERT"
8. You should see a new file `test.md` created on your Desktop

---

## 🚀 Quick Start Guide

### **Desktop Application**
1. Run `python3 markdown_magic_gui.py`
2. Click "ADD FILES" or drag files into the window
3. Select output folder
4. Configure OCR settings if needed  
5. Click "CONVERT"
6. Download converted files


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
- Try: `pip install --upgrade PyQt5`

### **Getting Help**
- 📧 Create an issue on GitHub
- 📖 Check the documentation in the `docs/` folder
- 🤝 Contribute improvements via pull requests

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Tesseract OCR** - For optical character recognition
- **PyQt5** - For the desktop GUI framework
- **PyMuPDF** - For PDF processing capabilities
- **All contributors** - For making this project better

---

**Made with ❤️ for the open source community**

*Transform your documents. Embrace the power of Markdown.* ✨# MarkdownMagic
