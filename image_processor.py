#!/usr/bin/env python3
"""
Image processing module for MarkdownMagic
Handles image extraction, OCR, and markdown placeholder creation
"""

import os
import io
from pathlib import Path
import subprocess

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not installed. Image processing will be limited.")
    print("Install with: pip install Pillow")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Warning: pytesseract not installed. OCR will be disabled.")
    print("Install with: pip install pytesseract")

class ImageProcessor:
    """Handles image extraction, processing, and OCR for document conversion"""
    
    def __init__(self, tesseract_path=None):
        """Initialize the image processor with optional Tesseract path"""
        self.tesseract_available = TESSERACT_AVAILABLE
        self.pil_available = PIL_AVAILABLE
        self.current_output_dir = None  # Track current output directory
        
        # Set Tesseract path if provided
        if tesseract_path and TESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            
        # Test if Tesseract is working
        if self.tesseract_available:
            try:
                # Try using subprocess to check Tesseract version
                result = subprocess.run(['tesseract', '--version'], 
                                       capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    version = result.stdout.split('\n')[0]
                    print(f"✓ Tesseract OCR available: {version}")
                    self.tesseract_available = True
                else:
                    # Try using pytesseract
                    version = pytesseract.get_tesseract_version()
                    print(f"✓ Tesseract OCR available via pytesseract: {version}")
                    self.tesseract_available = True
            except Exception as e:
                print(f"Warning: Tesseract OCR not available: {e}")
                self.tesseract_available = False
        else:
            print("Warning: Tesseract OCR not available: pytesseract not installed")
    
    def create_image_folder(self, output_file):
        """Create an image folder for the converted document"""
        output_dir = os.path.dirname(output_file)
        self.current_output_dir = output_dir  # Store for later use
        
        base_filename = os.path.splitext(os.path.basename(output_file))[0]
        image_folder_name = f"{base_filename}_images"
        image_folder_path = os.path.join(output_dir, image_folder_name)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)
            print(f"✓ Created image folder: {image_folder_path}")
        
        return image_folder_name
    
    def process_image(self, image_bytes, image_number, images_folder, position_info='', 
                     existing_alt='', existing_caption='', original_format='png'):
        """Process an image: save without conversion, and generate OCR alt text"""
        try:
            if not self.pil_available:
                raise ImportError("PIL/Pillow not installed - cannot process images")
                
            # Open image for OCR but don't modify it
            image = Image.open(io.BytesIO(image_bytes))
            
            # Generate filename with original extension
            image_filename = f"image_{image_number}.{original_format.lower()}"
            
            # Use the stored output directory
            if self.current_output_dir is None:
                raise ValueError("No output directory set. Call create_image_folder first.")
            
            image_folder_path = os.path.join(self.current_output_dir, images_folder)
            if not os.path.exists(image_folder_path):
                os.makedirs(image_folder_path)
            
            # Save original image bytes without conversion
            image_path = os.path.join(image_folder_path, image_filename)
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            print(f"✓ Saved image: {image_path}")
            
            # Generate alt text (use existing if provided)
            if existing_alt:
                alt_text = existing_alt
            elif existing_caption:
                alt_text = existing_caption
            else:
                alt_text = self.generate_alt_text(image, image_number, position_info)
            
            # Create markdown placeholder
            markdown_placeholder = f"![{alt_text}]({images_folder}/{image_filename})"
            
            return markdown_placeholder
            
        except Exception as e:
            print(f"Warning: Could not process image {image_number}: {e}")
            # Return a placeholder anyway
            alt_text = f"Image ({image_number}), {position_info}, Could not process image:"
            image_filename = f"image_{image_number}.{original_format.lower()}"
            return f"![{alt_text}]({images_folder}/{image_filename})"
    
    def create_markdown_placeholder(self, image_number, position_info, description, image_folder_name, original_format='png'):
        """Create a markdown placeholder for an image"""
        alt_text = f"Image ({image_number}), {position_info}, {description}:"
        image_filename = f"image_{image_number}.{original_format.lower()}"
        return f"![{alt_text}]({image_folder_name}/{image_filename})"
    
    def generate_alt_text(self, image, image_number, position_info):
        """Generate alt text for an image using OCR"""
        if not self.tesseract_available:
            return f"Image ({image_number}), {position_info}, OCR not available:"
        
        try:
            # Enhance image for better OCR
            enhanced_image = self.enhance_image_for_ocr(image.copy())
            
            # Try multiple OCR configurations
            ocr_text = ""
            
            # First try: Standard document OCR
            try:
                ocr_text = pytesseract.image_to_string(enhanced_image, config='--psm 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ').strip()
            except:
                pass
            
            # Second try: Single block of text
            if not ocr_text or len(ocr_text) < 3:
                try:
                    ocr_text = pytesseract.image_to_string(enhanced_image, config='--psm 6').strip()
                except:
                    pass
            
            # Third try: Single line of text
            if not ocr_text or len(ocr_text) < 3:
                try:
                    ocr_text = pytesseract.image_to_string(enhanced_image, config='--psm 7').strip()
                except:
                    pass
            
            # Clean up the OCR text
            ocr_text = ' '.join(ocr_text.split())  # Remove extra whitespace
            
            # Limit length and clean up
            if len(ocr_text) > 100:
                ocr_text = ocr_text[:97] + "..."
            
            # If OCR found text, use it
            if ocr_text and len(ocr_text) > 3:
                return f"Image ({image_number}), {position_info}, {ocr_text}:"
            else:
                return f"Image ({image_number}), {position_info}, Image content:"
                
        except Exception as e:
            print(f"Warning: OCR failed for image {image_number}: {e}")
            return f"Image ({image_number}), {position_info}, OCR failed:"
    
    def convert_to_png(self, image_bytes):
        """Convert image bytes to PNG format"""
        if not self.pil_available:
            return image_bytes  # Return original if PIL not available
            
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                # Keep transparency for RGBA
                pass
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save to bytes as PNG
            png_bytes = io.BytesIO()
            image.save(png_bytes, format='PNG')
            png_bytes.seek(0)
            
            return png_bytes.getvalue()
            
        except Exception as e:
            print(f"Warning: Could not convert image to PNG: {e}")
            return image_bytes  # Return original if conversion fails
    
    def process_image_file(self, image_file_path, output_file=None):
        """Process a standalone image file and generate OCR text"""
        if not os.path.exists(image_file_path):
            raise FileNotFoundError(f"Image file not found: {image_file_path}")
        
        if not self.pil_available:
            raise ImportError("PIL/Pillow not installed - cannot process images")
        
        try:
            # Open the image file
            image = Image.open(image_file_path)
            
            # Generate output filename if not provided
            if output_file is None:
                input_path = Path(image_file_path)
                output_file = str(input_path.with_suffix('.md'))
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Create image folder for this document
            images_folder = self.create_image_folder(output_file)
            
            # Read image as bytes for processing
            with open(image_file_path, 'rb') as f:
                image_bytes = f.read()
            
            # Get original format
            original_format = Path(image_file_path).suffix[1:]  # Remove the dot
            
            # Process the image (save without conversion and generate OCR)
            markdown_placeholder = self.process_image(
                image_bytes, 1, images_folder, f"from {os.path.basename(image_file_path)}", 
                original_format=original_format
            )
            
            # Generate OCR text
            ocr_text = ""
            if self.tesseract_available:
                try:
                    ocr_text = pytesseract.image_to_string(image, config='--psm 3').strip()
                    ocr_text = ' '.join(ocr_text.split())  # Clean whitespace
                except Exception as e:
                    print(f"Warning: OCR failed: {e}")
                    ocr_text = "OCR processing failed"
            
            # Write markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                # Add YAML frontmatter
                f.write("---\n")
                f.write(f'title: "{os.path.splitext(os.path.basename(image_file_path))[0]}"\n')
                f.write(f'source: "{image_file_path}"\n')
                f.write('converter: "MarkdownMagic"\n')
                f.write('type: "image"\n')
                f.write("---\n\n")
                
                # Add title
                f.write(f"# {os.path.splitext(os.path.basename(image_file_path))[0]}\n\n")
                
                # Add the image
                f.write(f"{markdown_placeholder}\n\n")
                
                # Add OCR text if available
                if ocr_text and len(ocr_text.strip()) > 0:
                    f.write("## Extracted Text (OCR)\n\n")
                    f.write(f"{ocr_text}\n\n")
                else:
                    f.write("*No text detected in image*\n\n")
            
            print(f"✓ Image file processed: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"! Error processing image file: {e}")
            raise
    
    def enhance_image_for_ocr(self, image):
        """Apply preprocessing to improve OCR accuracy"""
        if not self.pil_available:
            return image
        
        try:
            # Convert to grayscale for better OCR
            if image.mode != 'L':
                image = image.convert('L')
            
            # Increase contrast and brightness
            from PIL import ImageEnhance
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.2)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            return image
            
        except Exception as e:
            print(f"Warning: Could not enhance image for OCR: {e}")
            return image