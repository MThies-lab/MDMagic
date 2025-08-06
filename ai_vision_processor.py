#!/usr/bin/env python3
"""
AI Vision Processor for MarkdownMagic
Combines OCR with AI-powered image description generation
"""

import os
import io
import warnings
import hashlib
from pathlib import Path

# Suppress transformer warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not installed. Image processing will be limited.")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Warning: pytesseract not installed. OCR will be disabled.")

# Try to import AI vision models
try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    AI_VISION_AVAILABLE = True
    print("✓ AI Vision models available (BLIP)")
except ImportError:
    AI_VISION_AVAILABLE = False
    print("Note: transformers not installed. Install for AI image descriptions:")
    print("  pip3 install transformers torch")

class AIVisionProcessor:
    """Enhanced image processor with AI-powered description generation"""
    
    def __init__(self, tesseract_path=None, enable_ai=True, ai_model_size='base'):
        """
        Initialize the AI Vision processor
        
        Args:
            tesseract_path: Path to Tesseract executable
            enable_ai: Whether to enable AI image descriptions
            ai_model_size: 'base' or 'large' for AI model size
        """
        self.tesseract_available = TESSERACT_AVAILABLE
        self.pil_available = PIL_AVAILABLE
        self.ai_vision_available = AI_VISION_AVAILABLE and enable_ai
        self.current_output_dir = None
        
        # Image deduplication system
        self.image_hashes = {}  # hash -> (filename, alt_text, ai_description, ocr_text)
        self.image_counter = 0  # Track unique images only
        
        # Initialize Tesseract
        if tesseract_path and TESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Test Tesseract
        self._test_tesseract()
        
        # Initialize AI models
        self.ai_processor = None
        self.ai_model = None
        if self.ai_vision_available:
            self._initialize_ai_models(ai_model_size)
    
    def _test_tesseract(self):
        """Test if Tesseract is working"""
        if not self.tesseract_available:
            return
            
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract OCR available: {version}")
        except Exception as e:
            print(f"Warning: Tesseract OCR not available: {e}")
            self.tesseract_available = False
    
    def _initialize_ai_models(self, model_size='base'):
        """Initialize AI vision models"""
        try:
            print("Loading AI vision models... (this may take a moment)")
            
            if model_size == 'large':
                model_name = "Salesforce/blip-image-captioning-large"
            else:
                model_name = "Salesforce/blip-image-captioning-base"
            
            self.ai_processor = BlipProcessor.from_pretrained(model_name)
            self.ai_model = BlipForConditionalGeneration.from_pretrained(model_name)
            
            # Move to GPU if available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.ai_model = self.ai_model.to(device)
            
            print(f"✓ AI vision models loaded ({model_name}) on {device}")
            
        except Exception as e:
            print(f"Warning: Could not load AI vision models: {e}")
            self.ai_vision_available = False
    
    def create_image_folder(self, output_file):
        """Create an image folder for the converted document"""
        output_dir = os.path.dirname(output_file)
        self.current_output_dir = output_dir
        
        # Reset image cache for new document
        self.reset_image_cache()
        
        base_filename = os.path.splitext(os.path.basename(output_file))[0]
        image_folder_name = f"{base_filename}_images"
        image_folder_path = os.path.join(output_dir, image_folder_name)
        
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)
            print(f"✓ Created image folder: {image_folder_path}")
        
        return image_folder_name
    
    def reset_image_cache(self):
        """Reset the image deduplication cache for a new document"""
        self.image_hashes = {}
        self.image_counter = 0
        print("✓ Image deduplication cache reset")
    
    def process_image(self, image_bytes, image_number, images_folder, position_info='', 
                     existing_alt='', existing_caption='', original_format='png'):
        """Process an image with AI-powered description generation and deduplication"""
        try:
            if not self.pil_available:
                raise ImportError("PIL/Pillow not installed - cannot process images")
            
            # Calculate image hash for deduplication
            image_hash = self._calculate_image_hash(image_bytes)
            
            # Check if we've seen this image before
            if image_hash and image_hash in self.image_hashes:
                # Reuse existing image data
                cached_data = self.image_hashes[image_hash]
                cached_filename, cached_alt_text, cached_ai_desc, cached_ocr_text = cached_data
                
                print(f"✓ Duplicate image detected, reusing: {cached_filename}")
                
                # Update alt text with new position info but keep AI description
                updated_alt_text = self._update_alt_text_for_duplicate(
                    cached_alt_text, image_number, position_info
                )
                
                # Create markdown placeholder with cached filename
                return f"![{updated_alt_text}]({images_folder}/{cached_filename})"
            
            # New unique image - process normally
            self.image_counter += 1
            unique_number = self.image_counter
            
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Generate filename for unique image
            image_filename = f"image_{unique_number}.{original_format.lower()}"
            
            # Save image
            if self.current_output_dir is None:
                raise ValueError("No output directory set. Call create_image_folder first.")
            
            image_folder_path = os.path.join(self.current_output_dir, images_folder)
            if not os.path.exists(image_folder_path):
                os.makedirs(image_folder_path)
            
            image_path = os.path.join(image_folder_path, image_filename)
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            print(f"✓ Saved new unique image: {image_path}")
            
            # Generate smart alt text and extract components for caching
            alt_text = self._generate_smart_alt_text(
                image, image_number, position_info, existing_alt, existing_caption
            )
            
            # Extract AI description and OCR for caching
            ocr_text = self._extract_text_with_ocr(image)
            ai_description = self._generate_ai_description(image)
            
            # Cache the image data for future duplicates
            if image_hash:
                self.image_hashes[image_hash] = (image_filename, alt_text, ai_description, ocr_text)
            
            # Create markdown placeholder
            markdown_placeholder = f"![{alt_text}]({images_folder}/{image_filename})"
            
            return markdown_placeholder
            
        except Exception as e:
            print(f"Warning: Could not process image {image_number}: {e}")
            alt_text = f"Image ({image_number}), {position_info}, Processing error"
            image_filename = f"image_{image_number}.{original_format.lower()}"
            return f"![{alt_text}]({images_folder}/{image_filename})"
    
    def _generate_smart_alt_text(self, image, image_number, position_info, 
                                existing_alt='', existing_caption=''):
        """Generate intelligent alt text using OCR + AI"""
        
        # Use existing alt text if provided
        if existing_alt:
            return f"{existing_alt}"
        if existing_caption:
            return f"{existing_caption}"
        
        # Try OCR first (for text-heavy images)
        ocr_text = self._extract_text_with_ocr(image)
        
        # Try AI description (for visual content)
        ai_description = self._generate_ai_description(image)
        
        # Combine results intelligently
        return self._combine_descriptions(
            image_number, position_info, ocr_text, ai_description
        )
    
    def _extract_text_with_ocr(self, image):
        """Extract text from image using Tesseract OCR"""
        if not self.tesseract_available:
            return ""
        
        try:
            # Enhance image for better OCR
            enhanced_image = self._enhance_image_for_ocr(image.copy())
            
            # Try multiple OCR configurations
            ocr_configs = [
                '--psm 3',  # Fully automatic page segmentation
                '--psm 6',  # Single uniform block
                '--psm 7',  # Single text line
            ]
            
            for config in ocr_configs:
                try:
                    ocr_text = pytesseract.image_to_string(enhanced_image, config=config).strip()
                    ocr_text = ' '.join(ocr_text.split())  # Clean whitespace
                    
                    if ocr_text and len(ocr_text) > 3:
                        # Limit length
                        if len(ocr_text) > 150:
                            ocr_text = ocr_text[:147] + "..."
                        return ocr_text
                except:
                    continue
            
            return ""
            
        except Exception as e:
            print(f"Warning: OCR failed: {e}")
            return ""
    
    def _generate_ai_description(self, image):
        """Generate AI-powered image description"""
        if not self.ai_vision_available:
            return ""
        
        try:
            # Convert image to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Process image with AI model
            inputs = self.ai_processor(image, return_tensors="pt")
            
            # Move inputs to same device as model
            device = next(self.ai_model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Generate description with improved parameters
            with torch.no_grad():
                out = self.ai_model.generate(
                    **inputs, 
                    max_length=50, 
                    min_length=5,
                    num_beams=5,
                    no_repeat_ngram_size=2,  # Prevent repetitive n-grams
                    early_stopping=True,
                    do_sample=False  # Use beam search for consistency
                )
            
            description = self.ai_processor.decode(out[0], skip_special_tokens=True)
            
            # Clean up description
            description = description.strip()
            if description.lower().startswith('a picture of '):
                description = description[13:]  # Remove redundant prefix
            elif description.lower().startswith('an image of '):
                description = description[12:]
            
            return description
            
        except Exception as e:
            print(f"Warning: AI description failed: {e}")
            return ""
    
    def _combine_descriptions(self, image_number, position_info, ocr_text, ai_description):
        """Intelligently combine OCR and AI descriptions"""
        
        # Base prefix
        prefix = f"Image {image_number}"
        if position_info:
            prefix += f", {position_info}"
        
        # Prioritize descriptions
        if ocr_text and ai_description:
            # Both available - combine them
            return f"{prefix}, This image displays {ai_description}, Text: {ocr_text}"
        elif ocr_text:
            # Only OCR text available
            return f"{prefix}, Text content: {ocr_text}"
        elif ai_description:
            # Only AI description available
            return f"{prefix}, This image displays {ai_description}"
        else:
            # Neither available - generic description
            return f"{prefix}, Visual content"
    
    def _calculate_image_hash(self, image_bytes):
        """Calculate a perceptual hash for duplicate detection"""
        try:
            # Create a simple hash based on image content
            # This catches exact duplicates
            content_hash = hashlib.md5(image_bytes).hexdigest()
            
            # For more sophisticated duplicate detection, we could use perceptual hashing
            # but MD5 of content works well for exact duplicates (icons, logos, etc.)
            return content_hash
            
        except Exception as e:
            print(f"Warning: Could not calculate image hash: {e}")
            return None

    def _update_alt_text_for_duplicate(self, original_alt_text, new_image_number, new_position_info):
        """Update alt text for duplicate image with new position info"""
        try:
            # Parse original alt text to extract AI description
            if "This image displays" in original_alt_text:
                # Extract the AI description part
                parts = original_alt_text.split("This image displays", 1)
                if len(parts) > 1:
                    ai_desc_part = parts[1].split(", Text:")[0]  # Remove OCR text if present
                    
                    # Create new alt text with updated position
                    prefix = f"Image {new_image_number}"
                    if new_position_info:
                        prefix += f", {new_position_info}"
                    
                    return f"{prefix}, This image displays{ai_desc_part}"
            
            # Fallback: just update the image number
            return original_alt_text.replace("Image 1", f"Image {new_image_number}")
            
        except Exception as e:
            print(f"Warning: Could not update alt text for duplicate: {e}")
            return original_alt_text

    def _enhance_image_for_ocr(self, image):
        """Enhance image for better OCR results"""
        if not self.pil_available:
            return image
        
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance for OCR
            from PIL import ImageEnhance
            
            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            return image
            
        except Exception as e:
            print(f"Warning: Could not enhance image for OCR: {e}")
            return image
    
    def process_image_file(self, image_file_path, output_file=None, enable_ai=None):
        """Process a standalone image file with AI description"""
        if not os.path.exists(image_file_path):
            raise FileNotFoundError(f"Image file not found: {image_file_path}")
        
        if not self.pil_available:
            raise ImportError("PIL/Pillow not installed - cannot process images")
        
        # Override AI setting if specified
        original_ai_setting = self.ai_vision_available
        if enable_ai is not None:
            self.ai_vision_available = enable_ai and AI_VISION_AVAILABLE
        
        try:
            # Open image
            image = Image.open(image_file_path)
            
            # Generate output filename
            if output_file is None:
                input_path = Path(image_file_path)
                output_file = str(input_path.with_suffix('.md'))
            
            # Create directories
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Create image folder
            images_folder = self.create_image_folder(output_file)
            
            # Read image bytes
            with open(image_file_path, 'rb') as f:
                image_bytes = f.read()
            
            # Get original format
            original_format = Path(image_file_path).suffix[1:]
            
            # Process image with AI
            markdown_placeholder = self.process_image(
                image_bytes, 1, images_folder, f"from {os.path.basename(image_file_path)}", 
                original_format=original_format
            )
            
            # Generate comprehensive analysis
            ocr_text = self._extract_text_with_ocr(image)
            ai_description = self._generate_ai_description(image)
            
            # Write enhanced markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                # YAML frontmatter
                f.write("---\n")
                f.write(f'title: "{os.path.splitext(os.path.basename(image_file_path))[0]}"\n')
                f.write(f'source: "{image_file_path}"\n')
                f.write('converter: "MarkdownMagic AI"\n')
                f.write('type: "image"\n')
                f.write('features:\n')
                f.write(f'  ocr_enabled: {self.tesseract_available}\n')
                f.write(f'  ai_vision_enabled: {self.ai_vision_available}\n')
                f.write("---\n\n")
                
                # Title
                f.write(f"# {os.path.splitext(os.path.basename(image_file_path))[0]}\n\n")
                
                # Image
                f.write(f"{markdown_placeholder}\n\n")
                
                # AI Description
                if ai_description:
                    f.write("## AI Description\n\n")
                    f.write(f"**Visual Content:** This image displays {ai_description}\n\n")
                
                # OCR Results
                if ocr_text:
                    f.write("## Extracted Text (OCR)\n\n")
                    f.write(f"```\n{ocr_text}\n```\n\n")
                elif self.tesseract_available:
                    f.write("## Text Analysis\n\n")
                    f.write("*No readable text detected in this image*\n\n")
                
                # Technical Info
                f.write("## Technical Information\n\n")
                f.write(f"- **File:** {os.path.basename(image_file_path)}\n")
                f.write(f"- **Format:** {original_format.upper()}\n")
                f.write(f"- **Size:** {os.path.getsize(image_file_path)} bytes\n")
                f.write(f"- **OCR Engine:** {'Tesseract' if self.tesseract_available else 'Not available'}\n")
                f.write(f"- **AI Vision:** {'BLIP Model' if self.ai_vision_available else 'Not enabled'}\n")
            
            print(f"✓ Enhanced image processing complete: {output_file}")
            return output_file
            
        finally:
            # Restore original AI setting
            self.ai_vision_available = original_ai_setting
    
    def get_capabilities(self):
        """Return current processor capabilities"""
        return {
            'pil_available': self.pil_available,
            'tesseract_available': self.tesseract_available,
            'ai_vision_available': self.ai_vision_available,
            'features': {
                'image_processing': self.pil_available,
                'text_extraction': self.tesseract_available,
                'ai_descriptions': self.ai_vision_available,
                'smart_alt_text': True
            }
        }

# Convenience function for easy usage
def create_ai_processor(tesseract_path=None, enable_ai=True):
    """Create an AI vision processor with default settings"""
    return AIVisionProcessor(tesseract_path=tesseract_path, enable_ai=enable_ai)

if __name__ == "__main__":
    # Test the processor
    processor = create_ai_processor()
    caps = processor.get_capabilities()
    
    print("\n🔍 AI Vision Processor Capabilities:")
    print(f"📸 Image Processing: {'✓' if caps['pil_available'] else '✗'}")
    print(f"📝 Text Extraction (OCR): {'✓' if caps['tesseract_available'] else '✗'}")
    print(f"🤖 AI Image Descriptions: {'✓' if caps['ai_vision_available'] else '✗'}")
    print(f"🎯 Smart Alt Text: {'✓' if caps['features']['smart_alt_text'] else '✗'}")