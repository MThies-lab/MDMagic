
# 🚀 Markdown Magic Installation Guide

Transform any document into beautiful, structured Markdown with advanced batch processing, OCR capabilities, and intelligent format preservation.

Markdown Magic Transforms documents into modern, portable Markdown format for any use case, and preserves document structure, formatting, and embedded content. It follows the official Markdown Guide style guide by Matt Cone and features desktop GUI application and command line interface for embedded functionality. This program removes images from documents and places them in a separate cloned name folder, renaming the images in the order of their placement in the document. In the new markdown file, a placeholder for each image is generated in its place, clearly identifying which images belongs there. Additionally, the Tesseract OCR feature "reads" the image to generate a brief description of each image it scans, and is part of the image placeholder. This program supports drag and drop and standard file upload, as well as batch processing up to 250 mb. This program is completely free, completely local, and only has access to the folder the user designates to send the converted file to. 

**Note:** This project was created out of curiosity and necessity. If you find something that's broken, or could be better, please let me know! I built this either before the Markitdown MCP was live or before I knew about it. 

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

---

### 📄 **Supported File Formats**
|Document Type | Format |
|---------|----------------|
| **Text Documents** |  `.txt`, `.rtf`  | 
| **Microsoft Office** | `.docx`, `.doc`, `.xlsx`, `.xls`  | 
| **PDF Documents** |  `.pdf` (with OCR support) | 
| **Web Documents:** |  `.html`, `.htm` | 
| **Images:** |  `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.tif` | 
| **OpenDocument:** |  `.odt` | 


### ⚡ **Advanced Features**
 |Feature | Description |
 |------------------|-------------------------------------------|
 | Batch Processing |  Convert hundreds of files simultaneously | 
 | OCR Text Recognition |  Extract text from images and scanned PDFs | 
 | Multi-language OCR |  Support for 11+ languages including English, Spanish, French, German, Chinese, Japanese, Korean, Arabic | 
 | Smart Structure Detection:|  Automatically identify headings, lists, tables, and formatting | 
 | Image Extraction |  Save embedded images with proper linking | 
 | Format Preservation |  Maintain original document structure and styling | 
 | Progress Tracking |  Real-time conversion progress with detailed status | 
 | Error Handling | Robust error recovery and detailed reporting | 
 | Size Validation |  Intelligent file size limits (250MB batch limit) | 

## Markdown Magic Vs MCP Markitdown

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

## Prerequisites

### 📋 System Requirements

#### **Python Version**
 |----------|-----------------------|
 | Requirement/Status | Version |
 | Required |  Python 3.8 or higher | 
 | Recommended | Python 3.9 - 3.12 | 
 | Tested |  Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 | 

#### **Operating Systems**
 |---------|------------------|
 | OS | Version |
 | Windows |  10, 11 (64-bit) | 
 | macOS |  10.14+ (Mojave and newer) | 
 | Linux |  Ubuntu 18.04+, CentOS 7+, Debian 9+ | 

### **Hardware Requirements**
 |-----|------------------------------|
 | Component | Requirement |
 | RAM | 4GB minimum, 8GB recommended | 
 | Storage |  500MB free space | 
 | Processor |  Any modern CPU (OCR benefits from multi-core) | 

---

### 📦 Required Python Libraries

#### **Core Feature Dependencies**
 |-------------------------|--------------------------|
 | PyQt5>=5.15.0           |  # Desktop GUI framework | 
 | Pillow>=8.0.0           |  # Image processing | 
 | pytesseract>=0.3.7      |  # OCR text recognition | 
 | PyMuPDF>=1.18.0         |  # PDF processing | 
 | python-docx>=0.8.10     |  # Word document processing | 
 | beautifulsoup4>=4.9.0   |  # HTML parsing | 
 | striprtf>=0.0.15        |  # RTF document processing | 
 | openpyxl>=3.0.5         |  # Excel file processing | 
 | lxml>=4.6.0             |   # XML processing | 
 | tqdm>=4.60.0            |   # Progress bars | 


### **Development Dependencies**
 |-------------------------|-------------------------------------|
 | py2app>=0.28.0          |  # macOS app packaging (macOS only) | 


---

## 🛠️ Installation Guide

### **Verify Python Installation**

Verify Python installation:

 | **On Windows:**  | **On macOS:** | **On Linux:** |
 |------------------|---------------|---------------|
 | 1. Press `Windows Key + R`  | 1. Press `Cmd + Space` | 1. Press `Ctrl + Alt + T` | 
 | 2. Type `cmd` and press Enter | 2. Type `terminal` and press Enter | 2. Type: `python3 --version` |
 | 3. In the terminal window that opens, type: `python --version` | 3. In the terminal window, type: `python3 --version` | 3. Press Enter | 
 | 4. Press Enter | 4. Press Enter |  |

If the system displays an error, you must install Python.

---

### **Install Python **

|**Windows:** | **macOS:** |
|-------------|------------|
| 1. Go to https://python.org/downloads | 1. Go to https://python.org/downloads | 
| 2. Click "Download Python" (latest version) | 2. Download the latest Python version | 
| 3. Run the downloaded file | 3. Run the installer and follow prompts | 
| 4. **IMPORTANT:** Check "Add Python to PATH" during installation |  
| 5. Click "Install Now" | 

 **Linux (Ubuntu/Debian):** 
Run this command:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

### **Install Tesseract OCR (For Text Recognition)**

**Windows:**
1. Navigate to https://github.com/UB-Mannheim/tesseract/wiki
2. Download `Tesseract`.
3. Open your download folder and run the installer file.
4. Save the installation path in text file for reference (usually `C:\Program Files\Tesseract-OCR\`).

**macOS:**
1. Navigate to https://brew.sh
2. Install Homebrew.
3. Open Terminal and run this command:
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
1. Open your terminal and run this command:
```bash
sudo apt install tesseract-ocr
```

---

### **Download Markdown Magic**

**Option A: Download ZIP**
1. Navigate to: https://github.com/MThies-lab/Markdown-Magic
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Select the destination to send and extract the ZIP file. 

**Option B: Use Git (Advanced)**
1. Navigate to your terminal and run:
```bash
git clone https://github.com/MThies-lab/Markdown-Magic.git
cd Markdown-Magic
```

---

### **Open Terminal/Command Prompt in Project Folder**

| **Windows:** | **macOS:** | **Linux:** | 
|--------------|------------|------------|
1. Open File Explorer | 1. Open Finder | 1. Open your file manager | 
2. Navigate to your Markdown-Magic folder | 2. Navigate to your Markdown-Magic folder | 2. Navigate to the Markdown-Magic folder | 
3. Hold `Shift` and right-click in the folder | 3. Right-click the folder | 3. Right-click and select "Open in Terminal" | 
4. Select "Open PowerShell window here" or "Open command window here" | 4. Select "Services" → "New Terminal at Folder" |  | 

---

### **Create a Virtual Environment**

Creat a virtual environment to keep your project dependencies separate from other Python projects. Run these commands in your respective terminal window for your OS.


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

If successful, the terminal displays `(markdown_magic_env)` at the beginning of your command line.

---

### Install Required Libraries**

Run this command for your respective OS. This may take a few minutes to install.

**Windows:**
```cmd
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```


---

## **Test the Installation**

###**Run the desktop application:**
There are multiple ways to launch Markdown Magic. If successful, the system displays a retro, nostalgic black screen with green fonts and outlines.

1. Double click `markdown_magic_launcher.py` in your local repository. This launches the program.
2. Launch from the command line using the appropriate commands for your OS:

**Windows:**
```cmd
python markdown_magic_gui.py
```

**macOS/Linux:**
```bash
python3 markdown_magic_gui.py
```

---

### **Test a Sample File**

1. Create or select a document file. I recommend using a .pdf or .docx.
    a. This will show you immediately if it's working correctly, in comparison to a .txt file that doesn't have much, if any measurable formatting.
2. In Markdown Magic, click **ADD FILES** or Drag and Drop into the file window. 
7. Click **OUTPUT FOLDER**
8. Select a folder destination for the converted file.
9. Click **CONVERT**
10. When the system prompts you if you want open your output folder, click **Yes**.


##Troubleshooting

### **Common Issues**

**"Command not found" error:**
- Make sure Python is installed and added to PATH
- Try `python3` instead of `python` on macOS/Linux

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

## 🙏 Acknowledgments

- **Tesseract OCR** - For optical character recognition
- **PyQt5** - For the desktop GUI framework
- **PyMuPDF** - For PDF processing capabilities
- **All contributors** - For making this project better

---

**Made with ❤️ for the open source community**

*Transform your documents. Embrace the power of Markdown.* ✨# MarkdownMagic
