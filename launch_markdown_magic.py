#!/usr/bin/env python3
"""
EZ Markdown Converter - Launcher
Double-clickable launcher that works from GUI file managers
"""

import sys
import os
import platform
import traceback
import time

# Make sure the script runs from its own directory
if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))

print("=" * 60)
print("EZ MARKDOWN CONVERTER - STARTING")
print("=" * 60)

# Check for PyQt5
try:
    import PyQt5
    print("✓ PyQt5 found")
except ImportError:
    print("✗ PyQt5 not found")
    print("Install with: pip3 install PyQt5")
    print("\nRun this command to install: pip3 install PyQt5")
    time.sleep(5)  # Give user time to read message if double-clicking
    sys.exit(1)

# Check for document converter
try:
    from document_converter import DocumentConverter
    print("✓ DocumentConverter found")
except ImportError:
    print("! DocumentConverter not found (will use basic conversion)")

# Check for batch processor
try:
    from batch_processor import BatchProcessor
    print("✓ BatchProcessor found")
except ImportError:
    print("! BatchProcessor not found (will use single file conversion)")

# Check for image processor
try:
    from image_processor import ImageProcessor
    print("✓ ImageProcessor found")
except ImportError:
    print("! ImageProcessor not found (image extraction disabled)")

# Check for Tesseract OCR
tesseract_found = False
if platform.system() == "Windows":
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    # Check user-specific installation
    username = os.getenv('USERNAME', '')
    if username:
        user_path = rf"C:\Users\{username}\AppData\Local\Tesseract-OCR\tesseract.exe"
        possible_paths.append(user_path)
    
    for path in possible_paths:
        if os.path.exists(path):
            tesseract_found = True
            print(f"✓ Tesseract OCR found: {path}")
            break
else:
    # For macOS and Linux, check command availability
    try:
        import subprocess
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, check=False)
        if result.returncode == 0:
            tesseract_found = True
            version = result.stdout.split('\n')[0]
            print(f"✓ Tesseract OCR found: {version}")
    except:
        pass

if not tesseract_found:
    print("! Tesseract OCR not found (OCR for images will be limited)")
    if platform.system() == "Darwin":  # macOS
        print("  Install with: brew install tesseract")
    elif platform.system() == "Linux":
        print("  Install with: sudo apt-get install tesseract-ocr")
    else:
        print("  Download from: https://github.com/UB-Mannheim/tesseract/wiki")

# Launch the GUI
try:
    print("\n✓ Launching GUI...")
    from markdown_magic_gui import main
    exit_code = main()
    sys.exit(exit_code)
except Exception as e:
    print(f"✗ Error launching GUI: {e}")
    traceback.print_exc()
    print("\nPress Enter to exit...")
    try:
        input()  # This will work if run from terminal
    except EOFError:
        # If running by double-click, input() might fail with EOFError
        time.sleep(10)  # Give user time to read error
    sys.exit(1)
