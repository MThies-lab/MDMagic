#!/usr/bin/env python3
"""
Markdown Magic - Automated Build Script
Builds standalone applications for different platforms
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def run_command(command, description="Running command"):
    """Run a command and return success status"""
    print(f"\n→ {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ Success: {description}")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {description}")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("CHECKING DEPENDENCIES")
    
    dependencies = {
        'PyQt5': 'pip install PyQt5',
        'document_converter': 'Make sure document_converter.py is present',
        'batch_processor': 'Make sure batch_processor.py is present',
        'image_processor': 'Make sure image_processor.py is present'
    }
    
    all_good = True
    
    # Check Python packages
    try:
        import PyQt5
        print("✓ PyQt5 found")
    except ImportError:
        print("✗ PyQt5 not found - install with: pip install PyQt5")
        all_good = False
    
    # Check local modules
    for module in ['document_converter.py', 'batch_processor.py', 'image_processor.py']:
        if os.path.exists(module):
            print(f"✓ {module} found")
        else:
            print(f"✗ {module} not found")
            all_good = False
    
    return all_good

def create_launcher_if_needed():
    """Create the launcher file if it doesn't exist"""
    if not os.path.exists('launch_markdown_magic.py'):
        print("Creating launch_markdown_magic.py...")
        
        launcher_content = '''#!/usr/bin/env python3
"""
Markdown Magic - Launcher
"""

import sys
import os

# Add current directory to path
if os.path.dirname(__file__):
    os.chdir(os.path.dirname(__file__))
    sys.path.insert(0, os.path.dirname(__file__))

try:
    from ezmc_gui import main
    if __name__ == "__main__":
        sys.exit(main())
except ImportError as e:
    print(f"Error importing GUI: {e}")
    print("Make sure ezmc_gui.py is in the same directory")
    sys.exit(1)
'''
        
        with open('launch_markdown_magic.py', 'w') as f:
            f.write(launcher_content)
        print("✓ Created launch_markdown_magic.py")

def build_macos():
    """Build macOS application using py2app"""
    print_header("BUILDING MACOS APPLICATION")
    
    # Check if py2app is installed
    try:
        import py2app
        print("✓ py2app found")
    except ImportError:
        print("Installing py2app...")
        if not run_command("pip install py2app", "Installing py2app"):
            return False
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for directory in ['build', 'dist']:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"✓ Removed {directory}")
    
    # Build the application
    if run_command("python setup.py py2app", "Building macOS app with py2app"):
        print("✓ macOS application built successfully!")
        print("Application location: dist/Markdown Magic.app")
        
        # Optionally create DMG
        create_dmg = input("\nCreate DMG for distribution? (y/n): ").strip().lower()
        if create_dmg == 'y':
            create_macos_dmg()
        
        return True
    else:
        return False

def create_macos_dmg():
    """Create DMG file for macOS distribution"""
    print("\nCreating DMG...")
    
    # Check if create-dmg is available
    if run_command("which create-dmg", "Checking for create-dmg"):
        dmg_command = '''create-dmg \\
  --volname "Markdown Magic" \\
  --window-pos 200 120 \\
  --window-size 800 400 \\
  --icon-size 100 \\
  --icon "Markdown Magic.app" 200 190 \\
  --app-drop-link 600 185 \\
  "MarkdownMagic.dmg" \\
  "dist/Markdown Magic.app"'''
        
        if run_command(dmg_command, "Creating DMG"):
            print("✓ DMG created: MarkdownMagic.dmg")
        else:
            print("! DMG creation failed")
    else:
        print("! create-dmg not found. Install with: brew install create-dmg")

def build_windows():
    """Build Windows application using PyInstaller"""
    print_header("BUILDING WINDOWS APPLICATION")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for directory in ['build', 'dist']:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"✓ Removed {directory}")
    
    # Build the application
    pyinstaller_command = '''pyinstaller --onedir --windowed \\
  --name "Markdown Magic" \\
  --add-data "document_converter.py;." \\
  --add-data "batch_processor.py;." \\
  --add-data "image_processor.py;." \\
  --add-data "ezmc_gui.py;." \\
  launch_markdown_magic.py'''
    
    if run_command(pyinstaller_command, "Building Windows app with PyInstaller"):
        print("✓ Windows application built successfully!")
        print("Application location: dist/Markdown Magic/")
        return True
    else:
        return False

def build_linux():
    """Build Linux application using PyInstaller"""
    print_header("BUILDING LINUX APPLICATION")
    
    # Similar to Windows but for Linux
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for directory in ['build', 'dist']:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"✓ Removed {directory}")
    
    # Build the application
    pyinstaller_command = '''pyinstaller --onedir \\
  --name "markdown-magic" \\
  --add-data "document_converter.py:." \\
  --add-data "batch_processor.py:." \\
  --add-data "image_processor.py:." \\
  --add-data "ezmc_gui.py:." \\
  launch_markdown_magic.py'''
    
    if run_command(pyinstaller_command, "Building Linux app with PyInstaller"):
        print("✓ Linux application built successfully!")
        print("Application location: dist/markdown-magic/")
        return True
    else:
        return False

def build_web_apps():
    """Build/prepare web applications"""
    print_header("PREPARING WEB APPLICATIONS")
    
    # Check if web requirements are met
    web_requirements = ['streamlit', 'flask']
    missing = []
    
    for req in web_requirements:
        try:
            __import__(req)
            print(f"✓ {req} found")
        except ImportError:
            missing.append(req)
            print(f"✗ {req} not found")
    
    if missing:
        install_missing = input(f"\nInstall missing packages ({', '.join(missing)})? (y/n): ").strip().lower()
        if install_missing == 'y':
            install_command = f"pip install {' '.join(missing)}"
            if run_command(install_command, "Installing web dependencies"):
                print("✓ Web dependencies installed")
            else:
                print("✗ Failed to install web dependencies")
                return False
    
    # Create a simple run script for Streamlit
    streamlit_script = '''#!/bin/bash
# Markdown Magic - Streamlit Web App Runner
echo "Starting Markdown Magic Streamlit App..."
echo "Access the app at: http://localhost:8501"
streamlit run markdown_magic_streamlit.py --server.port=8501
'''
    
    with open('run_streamlit.sh', 'w') as f:
        f.write(streamlit_script)
    os.chmod('run_streamlit.sh', 0o755)
    print("✓ Created run_streamlit.sh")
    
    # Create a simple run script for Flask
    flask_script = '''#!/bin/bash
# Markdown Magic - Flask Web App Runner
echo "Starting Markdown Magic Flask App..."
echo "Access the app at: http://localhost:5000"
python markdown_magic_flask.py
'''
    
    with open('run_flask.sh', 'w') as f:
        f.write(flask_script)
    os.chmod('run_flask.sh', 0o755)
    print("✓ Created run_flask.sh")
    
    # Create Docker files
    create_docker_files()
    
    print("✓ Web applications prepared")
    return True

def create_docker_files():
    """Create Docker files for web deployment"""
    print("Creating Docker files...")
    
    # Dockerfile for Streamlit
    streamlit_dockerfile = '''FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    tesseract-ocr \\
    tesseract-ocr-eng \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "markdown_magic_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
'''
    
    with open('Dockerfile.streamlit', 'w') as f:
        f.write(streamlit_dockerfile)
    print("✓ Created Dockerfile.streamlit")
    
    # Dockerfile for Flask
    flask_dockerfile = '''FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    tesseract-ocr \\
    tesseract-ocr-eng \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000/health

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "markdown_magic_flask:app"]
'''
    
    with open('Dockerfile.flask', 'w') as f:
        f.write(flask_dockerfile)
    print("✓ Created Dockerfile.flask")
    
    # Docker Compose for both services
    docker_compose = '''version: '3.8'

services:
  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    volumes:
      - ./temp:/app/temp
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  flask:
    build:
      context: .
      dockerfile: Dockerfile.flask
    ports:
      - "5000:5000"
    volumes:
      - ./temp:/app/temp
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - streamlit
      - flask
    restart: unless-stopped
'''
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    print("✓ Created docker-compose.yml")

def create_updated_requirements():
    """Create updated requirements.txt with all dependencies"""
    print("Creating updated requirements.txt...")
    
    requirements = '''# Core GUI requirements (for standalone app)
PyQt5>=5.15.0

# Document conversion libraries
PyMuPDF>=1.18.0      # For PDF handling
python-docx>=0.8.10  # For DOCX handling
openpyxl>=3.0.5      # For XLSX handling
beautifulsoup4>=4.9.0 # For HTML handling
striprtf>=0.0.15     # For RTF handling
lxml>=4.6.0          # For XML processing

# Image processing
Pillow>=8.0.0        # For image manipulation
pytesseract>=0.3.7   # For OCR (requires Tesseract installation)

# Utilities
tqdm>=4.50.0         # For progress bars

# Web frameworks (optional - for web deployment)
streamlit>=1.28.0    # For Streamlit web app
flask>=2.3.0         # For Flask web app
gunicorn>=21.0.0     # For production Flask deployment

# Build tools (optional - for standalone app building)
py2app>=0.28.0       # For macOS app building
pyinstaller>=5.0.0   # For Windows/Linux app building

# Additional utilities
requests>=2.28.0     # For HTTP requests
chardet>=5.0.0       # For character encoding detection
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✓ Updated requirements.txt")

def main():
    """Main build function"""
    print_header("MARKDOWN MAGIC - BUILD SCRIPT")
    print("This script helps you build Markdown Magic for different platforms")
    
    # Check dependencies first
    if not check_dependencies():
        print("\n! Please install missing dependencies before building")
        return False
    
    # Create launcher if needed
    create_launcher_if_needed()
    
    # Create updated requirements
    create_updated_requirements()
    
    # Determine platform
    current_platform = platform.system().lower()
    print(f"\nDetected platform: {current_platform}")
    
    # Build options
    print("\nBuild Options:")
    print("1. Standalone Desktop App")
    print("2. Web Applications (Streamlit + Flask)")
    print("3. Both Desktop and Web")
    print("4. Just prepare files (no building)")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    success = True
    
    if choice in ['1', '3']:
        # Build desktop app
        if current_platform == 'darwin':  # macOS
            success &= build_macos()
        elif current_platform == 'windows':
            success &= build_windows()
        elif current_platform == 'linux':
            success &= build_linux()
        else:
            print(f"! Unsupported platform for desktop build: {current_platform}")
            success = False
    
    if choice in ['2', '3']:
        # Prepare web apps
        success &= build_web_apps()
    
    if choice == '4':
        # Just prepare files
        print_header("PREPARING FILES")
        create_updated_requirements()
        print("✓ Files prepared")
    
    # Final summary
    print_header("BUILD SUMMARY")
    if success:
        print("✅ Build completed successfully!")
        
        if choice in ['1', '3']:
            print("\n📱 Desktop App:")
            if current_platform == 'darwin':
                print("  - macOS app: dist/Markdown Magic.app")
                if os.path.exists('MarkdownMagic.dmg'):
                    print("  - DMG installer: MarkdownMagic.dmg")
            elif current_platform == 'windows':
                print("  - Windows app: dist/Markdown Magic/")
            elif current_platform == 'linux':
                print("  - Linux app: dist/markdown-magic/")
        
        if choice in ['2', '3']:
            print("\n🌐 Web Apps:")
            print("  - Streamlit: Run with 'streamlit run markdown_magic_streamlit.py'")
            print("  - Flask: Run with 'python markdown_magic_flask.py'")
            print("  - Docker: Use 'docker-compose up' for containerized deployment")
        
        print("\n📋 Next Steps:")
        print("  1. Test the built applications")
        print("  2. Distribute to users")
        print("  3. Set up monitoring and maintenance")
        print("  4. Check the deployment guide for hosting options")
        
    else:
        print("❌ Build failed. Check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        print("\nPress Enter to exit...")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n! Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n! Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)