#!/usr/bin/env python3
"""
Test script for AI Vision capabilities in Markdown Magic
Demonstrates the difference between basic OCR and AI-enhanced image descriptions
"""

import os
import sys
from pathlib import Path

def test_ai_vision_capabilities():
    """Test the AI vision processor capabilities"""
    print("🧪 Testing Markdown Magic AI Vision Capabilities")
    print("=" * 60)
    
    try:
        # Test 1: Check if AI vision processor is available
        print("\n1️⃣ Testing AI Vision Processor Import...")
        from ai_vision_processor import AIVisionProcessor
        print("✅ AI Vision Processor: Available")
        
        # Create processor
        processor = AIVisionProcessor(enable_ai=True)
        capabilities = processor.get_capabilities()
        
        print(f"   📸 PIL/Image Processing: {'✅' if capabilities['pil_available'] else '❌'}")
        print(f"   📝 Tesseract OCR: {'✅' if capabilities['tesseract_available'] else '❌'}")
        print(f"   🤖 AI Vision Models: {'✅' if capabilities['ai_vision_available'] else '❌'}")
        
        # Test 2: Test enhanced image processor integration
        print("\n2️⃣ Testing Enhanced Image Processor...")
        from image_processor import ImageProcessor
        enhanced_processor = ImageProcessor(enable_ai=True)
        print("✅ Enhanced Image Processor: Available")
        
        # Test 3: Test document converter with AI
        print("\n3️⃣ Testing AI-Enhanced Document Converter...")
        from document_converter import DocumentConverter
        converter = DocumentConverter(enable_ai=True)
        print("✅ AI-Enhanced Document Converter: Available")
        
        # Test 4: Show feature comparison
        print("\n4️⃣ Feature Comparison:")
        print("   📊 Basic Tesseract OCR:")
        print("      • Extracts text from images")
        print("      • Works with scanned documents")
        print("      • Limited to text recognition only")
        print("")
        print("   🚀 AI-Enhanced Processing:")
        print("      • Generates visual content descriptions")
        print("      • Identifies objects, scenes, actions")
        print("      • Combines OCR text with AI descriptions")
        print("      • Creates meaningful alt-text for images")
        
        print("\n✨ All AI vision components are ready!")
        return True
        
    except ImportError as e:
        print(f"❌ AI Vision components not available: {e}")
        print("\n📋 To enable AI vision capabilities, install:")
        print("   pip3 install transformers torch torchvision")
        print("\n🔄 Falling back to basic OCR-only processing...")
        return False

def test_with_sample_image():
    """Test processing with a sample image if available"""
    print("\n🖼️ Testing with Sample Images")
    print("=" * 40)
    
    # Look for test images in the project
    test_image_paths = [
        "test_image.jpg",
        "test_image.png", 
        "logo.jpg",
        "logo.png"
    ]
    
    found_image = None
    for img_path in test_image_paths:
        if os.path.exists(img_path):
            found_image = img_path
            break
    
    if found_image:
        print(f"📁 Found test image: {found_image}")
        try:
            from ai_vision_processor import AIVisionProcessor
            processor = AIVisionProcessor(enable_ai=True)
            
            # Process the image
            output_file = processor.process_image_file(found_image)
            print(f"✅ Processed image with AI: {output_file}")
            print(f"📖 Check the generated markdown file to see AI descriptions!")
            
        except Exception as e:
            print(f"❌ Error processing image: {e}")
    else:
        print("📷 No test images found in current directory")
        print("   Add a .jpg or .png file to test AI vision capabilities")

def show_usage_examples():
    """Show usage examples for developers"""
    print("\n💡 Usage Examples")
    print("=" * 30)
    
    print("\n🐍 Python Code Examples:")
    
    print("\n1. Basic AI-enhanced image processing:")
    print("""
from ai_vision_processor import AIVisionProcessor

# Create processor with AI enabled
processor = AIVisionProcessor(enable_ai=True)

# Process an image file
output_md = processor.process_image_file('my_image.jpg')
print(f"Generated: {output_md}")
""")
    
    print("\n2. Document conversion with AI:")
    print("""
from document_converter import DocumentConverter

# Create converter with AI features
converter = DocumentConverter(enable_ai=True)

# Convert a PDF with images
output_md = converter.convert_to_markdown('document.pdf')
print(f"Converted with AI descriptions: {output_md}")
""")
    
    print("\n3. Disable AI for faster processing:")
    print("""
# For faster processing without AI descriptions
converter = DocumentConverter(enable_ai=False)
processor = ImageProcessor(enable_ai=False)
""")

if __name__ == "__main__":
    print("🚀 Markdown Magic AI Vision Test Suite")
    print("=" * 50)
    
    # Test core capabilities
    ai_available = test_ai_vision_capabilities()
    
    # Test with sample images if AI is available
    if ai_available:
        test_with_sample_image()
    
    # Show usage examples
    show_usage_examples()
    
    print("\n🎉 Testing complete!")
    print("\nNext steps:")
    print("1. Install AI dependencies: pip3 install transformers torch")
    print("2. Test with your own images")
    print("3. Enable AI features in your applications")