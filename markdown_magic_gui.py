#!/usr/bin/env python3
"""
Markdown Magic (Markdown Converter) - Simplified Single-File GUI Application
CRT-themed interface that integrates with existing components
"""

import sys
import os
import subprocess
import platform
from pathlib import Path
import traceback

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
        QLabel, QPushButton, QProgressBar, QFileDialog,
        QListWidget, QListWidgetItem, QMessageBox, QStatusBar, QCheckBox
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    from PyQt5.QtGui import QFont, QIcon
    PYQT_AVAILABLE = True
except ImportError:
    print("PyQt5 not installed. Run: pip3 install PyQt5")
    PYQT_AVAILABLE = False

# Import local components - gracefully handle if not available
try:
    from document_converter import DocumentConverter
    CONVERTER_AVAILABLE = True
except ImportError:
    print("Warning: DocumentConverter not available")
    CONVERTER_AVAILABLE = False

try:
    from batch_processor import BatchProcessor
    BATCH_PROCESSOR_AVAILABLE = True
except ImportError:
    print("Warning: BatchProcessor not available")
    BATCH_PROCESSOR_AVAILABLE = False

class ConversionWorker(QThread):
    """Worker thread for file conversions"""
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    file_completed = pyqtSignal(str, bool, str)  # filename, success, message
    conversion_finished = pyqtSignal(bool, str)  # success, output_folder
    
    def __init__(self, files_to_convert, output_folder, tesseract_path=None, enable_ai=True):
        super().__init__()
        self.files_to_convert = files_to_convert
        self.output_folder = output_folder
        self.tesseract_path = tesseract_path
        self.enable_ai = enable_ai
        self.should_stop = False
    
    def run(self):
        """Run the conversion process"""
        try:
            if not self.files_to_convert or not self.output_folder:
                self.status_update.emit("NO FILES OR OUTPUT FOLDER")
                self.conversion_finished.emit(False, "")
                return
            
            # Use BatchProcessor if available, otherwise fallback to basic conversion
            if BATCH_PROCESSOR_AVAILABLE and CONVERTER_AVAILABLE:
                self.status_update.emit(f"CONVERTING {len(self.files_to_convert)} FILES...")
                
                # Initialize converter with AI setting
                converter = DocumentConverter(self.tesseract_path, enable_ai=self.enable_ai)
                
                # Initialize batch processor
                batch_processor = BatchProcessor()
                
                # Define progress callback for batch processor
                def progress_callback(current, total, current_file, stage="converting"):
                    # Calculate more granular progress based on stage
                    base_progress = ((current - 1) / total) * 100
                    stage_progress = 0
                    
                    if stage == "starting":
                        stage_progress = 0
                        status_msg = f"STARTING {current}/{total}: {os.path.basename(current_file)}"
                    elif stage == "converting": 
                        stage_progress = 25  # 25% into current file
                        status_msg = f"PROCESSING {current}/{total}: {os.path.basename(current_file)}"
                    elif stage == "completed":
                        stage_progress = 100 / total  # Full file progress
                        status_msg = f"COMPLETED {current}/{total}: {os.path.basename(current_file)}"
                    elif stage == "failed":
                        stage_progress = 100 / total
                        status_msg = f"FAILED {current}/{total}: {os.path.basename(current_file)}"
                    else:
                        stage_progress = 50
                        status_msg = f"PROCESSING {current}/{total}: {os.path.basename(current_file)}"
                    
                    progress = int(base_progress + stage_progress)
                    progress = min(progress, 100)  # Cap at 100%
                    
                    self.progress_update.emit(progress)
                    self.status_update.emit(status_msg)
                
                # Process the batch
                result = batch_processor.process_batch(
                    self.files_to_convert, 
                    self.output_folder,
                    converter,
                    progress_callback
                )
                
                # Report results
                self.progress_update.emit(100)
                
                if result.successful_files:
                    success_msg = f"CONVERSION COMPLETE! {len(result.successful_files)}/{result.total_files} FILES CONVERTED"
                    self.status_update.emit(success_msg)
                    
                    # Emit file completed signals
                    for file_path in result.successful_files:
                        filename = os.path.basename(file_path)
                        self.file_completed.emit(filename, True, "CONVERSION SUCCESSFUL")
                    
                    # Emit signals for failed files
                    for file_path, error in result.failed_files:
                        filename = os.path.basename(file_path)
                        self.file_completed.emit(filename, False, error)
                    
                    self.conversion_finished.emit(True, self.output_folder)
                else:
                    self.status_update.emit("NO FILES WERE CONVERTED SUCCESSFULLY")
                    self.conversion_finished.emit(False, "")
            
            else:
                # Fallback to basic conversion if components not available
                self.status_update.emit("USING BASIC CONVERSION (COMPONENTS NOT AVAILABLE)")
                
                successful_conversions = 0
                total_files = len(self.files_to_convert)
                
                for i, file_path in enumerate(self.files_to_convert):
                    if self.should_stop:
                        break
                    
                    try:
                        # Update progress with more detail
                        filename = os.path.basename(file_path)
                        
                        # Starting file
                        progress = int((i / total_files) * 100)
                        self.progress_update.emit(progress)
                        self.status_update.emit(f"STARTING {i+1}/{total_files}: {filename}")
                        
                        # Processing file
                        progress = int((i / total_files) * 100 + 25)  # Add 25% for processing
                        progress = min(progress, 100)
                        self.progress_update.emit(progress)
                        self.status_update.emit(f"PROCESSING {i+1}/{total_files}: {filename}")
                        
                        # Basic conversion - create markdown file
                        base_name = os.path.splitext(filename)[0]
                        output_file = os.path.join(self.output_folder, f"{base_name}.md")
                        
                        # Simple text extraction
                        self.simple_convert_file(file_path, output_file)
                        
                        # Completion progress
                        progress = int(((i + 1) / total_files) * 100)
                        self.progress_update.emit(progress)
                        self.status_update.emit(f"COMPLETED {i+1}/{total_files}: {filename}")
                        
                        successful_conversions += 1
                        self.file_completed.emit(filename, True, "BASIC CONVERSION SUCCESSFUL")
                        
                    except Exception as e:
                        self.file_completed.emit(filename, False, str(e))
                
                # Final progress update
                self.progress_update.emit(100)
                
                if successful_conversions > 0:
                    self.status_update.emit(f"CONVERSION COMPLETE! {successful_conversions}/{total_files} FILES CONVERTED")
                    self.conversion_finished.emit(True, self.output_folder)
                else:
                    self.status_update.emit("NO FILES WERE CONVERTED SUCCESSFULLY")
                    self.conversion_finished.emit(False, "")
                
        except Exception as e:
            self.status_update.emit(f"CONVERSION FAILED: {str(e)}")
            print(f"Conversion error: {e}")
            traceback.print_exc()
            self.conversion_finished.emit(False, "")
    
    def simple_convert_file(self, input_file, output_file):
        """Simple file conversion for fallback mode"""
        try:
            # Get file extension
            file_ext = os.path.splitext(input_file)[1].lower()
            filename = os.path.basename(input_file)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write YAML frontmatter
                f.write("---\n")
                f.write(f'title: "{os.path.splitext(filename)[0]}"\n')
                f.write(f'source: "{input_file}"\n')
                f.write('converter: "Markdown Magic"\n')
                f.write("---\n\n")
                
                f.write(f"# {os.path.splitext(filename)[0]}\n\n")
                
                if file_ext == '.txt':
                    # For TXT files, copy content directly
                    try:
                        with open(input_file, 'r', encoding='utf-8') as txt_file:
                            content = txt_file.read()
                            f.write(content)
                    except:
                        f.write("*Could not read text file content*\n")
                
                elif file_ext in ['.html', '.htm']:
                    # Basic HTML to text conversion
                    try:
                        with open(input_file, 'r', encoding='utf-8') as html_file:
                            content = html_file.read()
                            # Very basic HTML tag removal
                            import re
                            text_content = re.sub(r'<[^>]+>', '', content)
                            text_content = re.sub(r'\s+', ' ', text_content).strip()
                            f.write(text_content)
                    except:
                        f.write("*Could not read HTML file content*\n")
                
                elif file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif']:
                    # Handle image files with AI processing
                    try:
                        from ai_vision_processor import AIVisionProcessor
                        processor = AIVisionProcessor(enable_ai=True)
                        # Process the image file directly, overwriting our basic output
                        result = processor.process_image_file(input_file, output_file)
                        return  # Skip the rest since AI processor handled everything
                    except ImportError:
                        f.write(f"*Image file: {filename}*\n\n")
                        f.write(f"![{filename}]({input_file})\n\n")
                        f.write("Note: For AI-powered image descriptions and OCR, install AI dependencies:\n")
                        f.write("```\npip3 install transformers torch\n```\n\n")
                    except Exception as e:
                        f.write(f"*Image processing failed: {e}*\n\n")
                        f.write(f"![{filename}]({input_file})\n\n")
                
                else:
                    # For other file types, create a placeholder
                    f.write(f"*File converted from {file_ext.upper()} format*\n\n")
                    f.write("Note: This is a basic conversion. For full functionality with advanced processing, ")
                    f.write("please ensure all converter modules are installed.\n\n")
                    
                    try:
                        file_size = os.path.getsize(input_file)
                        f.write(f"Original file size: {file_size} bytes\n")
                    except:
                        pass
                        
        except Exception as e:
            # If conversion fails, create error file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("---\n")
                f.write(f'title: "Conversion Error - {os.path.basename(input_file)}"\n')
                f.write('converter: "Markdown Magic"\n')
                f.write("---\n\n")
                f.write(f"# Conversion Error\n\n")
                f.write(f"Could not convert file: {input_file}\n")
                f.write(f"Error: {str(e)}\n")
    
    def stop(self):
        """Stop the conversion process"""
        self.should_stop = True

class DragDropFileList(QListWidget):
    """File list with drag and drop support"""
    
    files_dropped = pyqtSignal(list)
    file_removed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DropOnly)
        self.setFont(QFont("Courier New", 11))
        self.add_placeholder()
        
        # Set selection mode to allow single selection
        self.setSelectionMode(QListWidget.SingleSelection)
        
        # Enable context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)
            event.acceptProposedAction()
    
    def add_placeholder(self):
        if self.count() == 0:
            item = QListWidgetItem("Drop files here or use the Add Files button")
            item.setFlags(Qt.NoItemFlags)
            item.setData(Qt.UserRole, None)
            font = QFont("Courier New", 11)
            font.setItalic(True)
            item.setFont(font)
            self.addItem(item)
    
    def add_file_item(self, file_path):
        # Remove placeholder
        if self.count() > 0:
            first_item = self.item(0)
            if first_item and first_item.data(Qt.UserRole) is None:
                self.takeItem(0)
        
        filename = os.path.basename(file_path)
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                size_str = f"{size}B"
            elif size < 1024 * 1024:
                size_str = f"{size/1024:.1f}KB"
            else:
                size_str = f"{size/(1024*1024):.1f}MB"
        except:
            size_str = "???B"
        
        item = QListWidgetItem(f"{filename} ({size_str})")
        item.setToolTip(file_path)
        item.setData(Qt.UserRole, file_path)
        item.setFont(QFont("Courier New", 11))
        self.addItem(item)
    
    def get_all_file_paths(self):
        files = []
        for i in range(self.count()):
            item = self.item(i)
            if item and item.data(Qt.UserRole):
                files.append(item.data(Qt.UserRole))
        return files
    
    def clear_all_files(self):
        self.clear()
        self.add_placeholder()
    
    def has_files(self):
        for i in range(self.count()):
            item = self.item(i)
            if item and item.data(Qt.UserRole):
                return True
        return False
    
    def show_context_menu(self, position):
        """Show context menu for file operations"""
        item = self.itemAt(position)
        if item and item.data(Qt.UserRole):  # Only show menu for actual files
            from PyQt5.QtWidgets import QMenu, QAction
            
            menu = QMenu(self)
            
            # Remove file action
            remove_action = QAction("Remove File", self)
            remove_action.triggered.connect(lambda: self.remove_file(item))
            menu.addAction(remove_action)
            
            # Show menu at cursor position
            menu.exec_(self.mapToGlobal(position))
    
    def remove_file(self, item):
        """Remove a specific file from the list"""
        if item and item.data(Qt.UserRole):
            row = self.row(item)
            self.takeItem(row)
            
            # If no files left, add placeholder
            if not self.has_files():
                self.add_placeholder()
            
            # Emit signal to update parent
            self.file_removed.emit()
    
    def remove_selected_file(self):
        """Remove the currently selected file"""
        current_item = self.currentItem()
        if current_item and current_item.data(Qt.UserRole):
            self.remove_file(current_item)
    
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        from PyQt5.QtCore import Qt
        
        # Delete key removes selected file
        if event.key() == Qt.Key_Delete:
            self.remove_selected_file()
        else:
            super().keyPressEvent(event)

class MarkdownMagicWindow(QMainWindow):
    """Main application window with CRT theme"""
    
    def __init__(self):
        super().__init__()
        self.output_folder = None
        self.conversion_worker = None
        
        # Try to find Tesseract path (for OCR)
        self.tesseract_path = self.find_tesseract_path()
        
        self.init_ui()
        self.apply_crt_theme()
        
    def find_tesseract_path(self):
        """Find Tesseract installation on Windows"""
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
                return path
        
        # If not found, return None and let user specify later
        return None
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Markdown Magic")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Application Title
        title_label = QLabel("MARKDOWN MAGIC")
        title_font = QFont("Courier New", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Browse or drag and drop files to convert to markdown")
        subtitle_font = QFont("Courier New", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setObjectName("subtitle")
        main_layout.addWidget(subtitle_label)
        
        # Spacing
        main_layout.addSpacing(10)

        # AI Vision toggle
        self.ai_vision_checkbox = QCheckBox("Enable to generate alt-text for images automatically during conversion. Disable to disregard auto-alt text and increase conversion speed. This feature is enabled by default.")
        self.ai_vision_checkbox.setChecked(True)  # Default enabled
        self.ai_vision_checkbox.setFont(QFont("Courier New", 10))
        self.ai_vision_checkbox.setObjectName("ai_checkbox")
        main_layout.addWidget(self.ai_vision_checkbox)
        
        # Spacing
        main_layout.addSpacing(10)

        # Buttons Row 1: Add Files, Output Folder
        buttons1_layout = QHBoxLayout()
        
        self.add_files_btn = QPushButton("ADD FILES")
        self.add_files_btn.clicked.connect(self.add_files)
        self.add_files_btn.setObjectName("crt_button")
        buttons1_layout.addWidget(self.add_files_btn)
        
        self.output_folder_btn = QPushButton("OUTPUT FOLDER")
        self.output_folder_btn.clicked.connect(self.select_output_folder)
        self.output_folder_btn.setObjectName("crt_button")
        buttons1_layout.addWidget(self.output_folder_btn)
        
        main_layout.addLayout(buttons1_layout)
        
        # Output folder display
        self.output_folder_label = QLabel("You must select an Output Folder to continue")
        self.output_folder_label.setFont(QFont("Courier New", 10))
        self.output_folder_label.setAlignment(Qt.AlignCenter)
        self.output_folder_label.setObjectName("crt_button")
        main_layout.addWidget(self.output_folder_label)
        
        # Drag and Drop Window
        self.file_list = DragDropFileList()
        self.file_list.files_dropped.connect(self.add_files_to_list)
        self.file_list.file_removed.connect(self.on_file_removed)
        self.file_list.setMinimumHeight(200)
        self.file_list.setObjectName("drag_drop_area")
        main_layout.addWidget(self.file_list)
        
        
        # Buttons Row 2: Clear Files, Convert
        buttons2_layout = QHBoxLayout()
        
        self.clear_files_btn = QPushButton("CLEAR FILES")
        self.clear_files_btn.clicked.connect(self.clear_all_files)
        self.clear_files_btn.setEnabled(False)
        self.clear_files_btn.setObjectName("crt_button")
        buttons2_layout.addWidget(self.clear_files_btn)
        
        self.convert_btn = QPushButton("CONVERT")
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        self.convert_btn.setObjectName("convert_button")
        buttons2_layout.addWidget(self.convert_btn)
        
        main_layout.addLayout(buttons2_layout)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        main_layout.addWidget(self.progress_bar)
        
        # File info
        self.file_info_label = QLabel("No files selected")
        self.file_info_label.setFont(QFont("Courier New", 10))
        self.file_info_label.setAlignment(Qt.AlignCenter)
        self.file_info_label.setObjectName("info_label")
        main_layout.addWidget(self.file_info_label)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("READY")
        self.status_bar.setFont(QFont("Courier New", 10))
        
    def apply_crt_theme(self):
        """Apply the CRT hacker green theme"""
        self.setStyleSheet("""
            /* Main window background */
            QMainWindow {
                background-color: #000000;
                color: #00ff00;
            }
            
            /* Title styling */
            QLabel#title {
                color: #00ff00;
                background-color: #000000;
                border: 2px solid #00ff00;
                padding: 10px;
                text-align: center;
            }
            
            /* Subtitle styling */
            QLabel#subtitle {
                color: #00ff00;
                background-color: #000000;
            }
            
            /* Info labels */
            QLabel#info_label {
                color: #00ff00;
                background-color: #000000;
            }
            
            /* Buttons */
            QPushButton#crt_button {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 10px 20px;
                font-family: "Courier New";
                font-size: 12px;
                font-weight: bold;
                min-height: 20px;
            }
            
            QPushButton#crt_button:hover {
                background-color: #001100;
                color: #00ff00;
                border: 2px solid #00ff00;
            }
            
            QPushButton#crt_button:pressed {
                background-color: #00ff00;
                color: #000000;
                border: 2px solid #00ff00;
            }
            
            QPushButton#crt_button:disabled {
                background-color: #000000;
                color: #003300;
                border: 2px solid #003300; 
            }
            
            /* Convert button (special highlight) */
            QPushButton#convert_button {
                background-color: #000000;
                color: #00ff00;
                border: 3px solid #00ff00;
                padding: 10px 20px;
                font-family: "Courier New";
                font-size: 14px;
                font-weight: bold;
                min-height: 25px;
            }
            
            QPushButton#convert_button:hover {
                background-color: #002200;
                color: #00ff00;
                border: 3px solid #00ff00;
            }
            
            QPushButton#convert_button:pressed {
                background-color: #00ff00;
                color: #000000;
                border: 3px solid #00ff00;
            }
            
            QPushButton#convert_button:disabled {
                background-color: #000000;
                color: #003300;
                border: 3px solid #003300;
            }
            
            /* Drag and drop area */
            QListWidget#drag_drop_area {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                font-family: "Courier New";
                font-size: 11px;
                selection-background-color: #004400;
                selection-color: #00ff00;
            }
            
            QListWidget#drag_drop_area::item {
                padding: 5px;
                border-bottom: 1px solid #003300;
            }
            
            QListWidget#drag_drop_area::item:selected {
                background-color: #004400;
                color: #00ff00;
            }
            
            QListWidget#drag_drop_area::item:hover {
                background-color: #002200;
                color: #00ff00;
            }
            
            /* Progress bar */
            QProgressBar#progress_bar {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                text-align: center;
                font-family: "Courier New";
                font-size: 11px;
                font-weight: bold;
            }
            
            QProgressBar#progress_bar::chunk {
                background-color: #00ff00;
            }
            
            /* Status bar */
            QStatusBar {
                background-color: #000000;
                color: #00ff00;
                border-top: 1px solid #00ff00;
            }
            
            /* AI Vision Checkbox */
            QCheckBox#ai_checkbox {
                background-color: #000000;
                color: #00ff00;
                font-family: "Courier New";
                font-size: 11px;
                spacing: 5px;
            }
            
            QCheckBox#ai_checkbox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #00ff00;
                background-color: #000000;
            }
            
            QCheckBox#ai_checkbox::indicator:checked {
                background-color: #00ff00;
                border: 2px solid #00ff00;
            }
            
            QCheckBox#ai_checkbox::indicator:hover {
                border: 2px solid #00ff88;
            }
            
            /* Central widget */
            QWidget {
                background-color: #000000;
                color: #00ff00;
                font-family: "Courier New";
            }
        """)
    
    def add_files(self):
        """Open file dialog to add files"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select files to convert",
            "",
            "Supported files (*.txt *.pdf *.docx *.odt *.rtf *.html *.htm *.xlsx *.xls);;All files (*.*)"
        )
        
        if files:
            self.add_files_to_list(files)
    
    def add_files_to_list(self, files):
        """Add files to the conversion list"""
        added_count = 0
        current_files = self.file_list.get_all_file_paths()
        
        for file_path in files:
            if file_path not in current_files:
                self.file_list.add_file_item(file_path)
                added_count += 1
        
        if added_count > 0:
            self.update_file_info()
            self.update_convert_button_state()
            self.status_bar.showMessage(f"ADDED {added_count} FILE(S)")
    
    def clear_all_files(self):
        """Clear all files from the list"""
        self.file_list.clear_all_files()
        self.update_file_info()
        self.update_convert_button_state()
        self.status_bar.showMessage("CLEARED ALL FILES")
    
    def on_file_removed(self):
        """Handle individual file removal"""
        self.update_file_info()
        self.update_convert_button_state()
        self.status_bar.showMessage("FILE REMOVED")
    
    def update_file_info(self):
        """Update file information display"""
        file_paths = self.file_list.get_all_file_paths()
        count = len(file_paths)
        
        if count == 0:
            self.file_info_label.setText("No files selected")
            self.clear_files_btn.setEnabled(False)
        else:
            # Calculate total size
            total_size = 0
            for file_path in file_paths:
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    pass
            
            size_mb = total_size / (1024 * 1024)
            self.file_info_label.setText(f"{count} file(s) selected, {size_mb:.1f} MB total")
            self.clear_files_btn.setEnabled(True)
            
            # Check size limit
            if size_mb > 250:
                self.file_info_label.setText(f"{count} file(s) selected, {size_mb:.1f} MB total (EXCEEDS 250MB LIMIT)")
    
    def select_output_folder(self):
        """Select output folder with option to create new folder on desktop"""
        msg = QMessageBox()
        msg.setWindowTitle("Select Output Folder")
        msg.setText("Choose output folder option:")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #000000;
                color: #00ff00;
                font-family: "Courier New";
            }
            QMessageBox QPushButton {
                background-color: #000000;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 5px 15px;
                font-family: "Courier New";
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #001100;
            }
        """)
        
        existing_btn = msg.addButton("Browse Existing Folder", QMessageBox.ActionRole)
        desktop_btn = msg.addButton("Create New Folder on Desktop", QMessageBox.ActionRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)
        
        msg.exec_()
        
        if msg.clickedButton() == existing_btn:
            folder = QFileDialog.getExistingDirectory(self, "Select output folder")
            if folder:
                self.output_folder = folder
                self.output_folder_label.setText(f"Output: {folder}")
                self.update_convert_button_state()
                self.status_bar.showMessage("OUTPUT FOLDER SET")
                
        elif msg.clickedButton() == desktop_btn:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            folder_name = "Markdown_Magic_Conversions"
            new_folder_path = os.path.join(desktop_path, folder_name)
            
            counter = 1
            while os.path.exists(new_folder_path):
                new_folder_path = os.path.join(desktop_path, f"{folder_name}_{counter}")
                counter += 1
            
            try:
                os.makedirs(new_folder_path)
                self.output_folder = new_folder_path
                self.output_folder_label.setText(f"Output: {new_folder_path}")
                self.update_convert_button_state()
                self.status_bar.showMessage("NEW FOLDER CREATED ON DESKTOP")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create folder: {str(e)}")
    
    def update_convert_button_state(self):
        """Update the convert button state"""
        can_convert = (
            self.file_list.has_files() and 
            self.output_folder is not None and
            self.conversion_worker is None
        )
        self.convert_btn.setEnabled(can_convert)
    
    def start_conversion(self):
        """Start the conversion process"""
        file_paths = self.file_list.get_all_file_paths()
        
        if not file_paths or not self.output_folder:
            return
        
        # Disable UI elements
        self.convert_btn.setEnabled(False)
        self.add_files_btn.setEnabled(False)
        self.clear_files_btn.setEnabled(False)
        self.output_folder_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.status_bar.showMessage("STARTING CONVERSION...")
        
        # Start worker thread
        ai_enabled = self.ai_vision_checkbox.isChecked()
        self.conversion_worker = ConversionWorker(
            file_paths, 
            self.output_folder,
            self.tesseract_path,
            ai_enabled
        )
        
        # Connect signals
        self.conversion_worker.progress_update.connect(self.progress_bar.setValue)
        self.conversion_worker.status_update.connect(self.status_bar.showMessage)
        self.conversion_worker.file_completed.connect(self.on_file_completed)
        self.conversion_worker.conversion_finished.connect(self.on_conversion_finished)
        
        # Start the worker
        self.conversion_worker.start()
    
    def on_file_completed(self, filename, success, message):
        """Handle individual file completion"""
        # Could enhance with a conversion log display
        pass
    
    def on_conversion_finished(self, success, output_folder):
        """Handle conversion completion"""
        # Re-enable UI elements
        self.convert_btn.setEnabled(True)
        self.add_files_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(True)
        self.output_folder_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Clean up worker
        if self.conversion_worker:
            self.conversion_worker.deleteLater()
            self.conversion_worker = None
        
        # Update UI state
        self.update_convert_button_state()
        
        if success:
            self.status_bar.showMessage("CONVERSION COMPLETE")
            
            # Show completion dialog
            msg = QMessageBox()
            msg.setWindowTitle("Conversion Complete")
            msg.setText("Conversion complete. Open Output Folder?")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #000000;
                    color: #00ff00;
                    font-family: "Courier New";
                    font-size: 12px;
                }
                QMessageBox QPushButton {
                    background-color: #000000;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    padding: 8px 20px;
                    font-family: "Courier New";
                    font-weight: bold;
                    font-size: 11px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #001100;
                }
            """)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            
            if msg.exec_() == QMessageBox.Yes and output_folder:
                self.open_output_folder(output_folder)
        else:
            self.status_bar.showMessage("CONVERSION FAILED")
    
    def open_output_folder(self, folder_path):
        """Open the output folder in file explorer"""
        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", folder_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open folder: {str(e)}")

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("EZ Markdown Converter")
    app.setApplicationVersion("1.0")
    
    # Check if PyQt is available
    if not PYQT_AVAILABLE:
        print("ERROR: PyQt5 is not installed. Please install PyQt5 with: pip3 install PyQt5")
        return 1
    
    # Check for components
    if not CONVERTER_AVAILABLE:
        print("WARNING: DocumentConverter not available. Basic conversion will be used.")
        
    if not BATCH_PROCESSOR_AVAILABLE:
        print("WARNING: BatchProcessor not available. Single file conversion will be used.")
    
    # Create and show the main window
    window = MarkdownMagicWindow()
    window.show()
    
    # Run the application
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
