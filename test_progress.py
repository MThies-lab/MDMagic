#!/usr/bin/env python3
"""
Test script to demonstrate improved progress reporting
"""

import os
import sys
import tempfile
from batch_processor import BatchProcessor
from document_converter import DocumentConverter

def test_progress_reporting():
    """Test the improved progress reporting system"""
    print("🚀 Testing Improved Progress Reporting")
    print("=" * 50)
    
    # Create temp output folder
    output_folder = tempfile.mkdtemp()
    print(f"Output folder: {output_folder}")
    
    def detailed_progress_callback(current, total, current_file, stage='converting'):
        """Enhanced progress callback showing detailed status"""
        filename = os.path.basename(current_file)
        base_progress = ((current - 1) / total) * 100
        
        stage_progress_map = {
            'starting': 0,
            'converting': 25, 
            'completed': 100/total,
            'failed': 100/total
        }
        
        stage_progress = stage_progress_map.get(stage, 25)
        progress = int(base_progress + stage_progress)
        progress = min(progress, 100)
        
        # Create visual progress bar
        bar_length = 30
        filled_length = int(bar_length * progress / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        status_colors = {
            'starting': '🟡',
            'converting': '🔵', 
            'completed': '🟢',
            'failed': '🔴'
        }
        
        icon = status_colors.get(stage, '⚪')
        
        print(f"{icon} [{bar}] {progress:3d}% | {stage.upper():<10} | {current}/{total} | {filename}")
    
    try:
        # Initialize converter and processor
        converter = DocumentConverter(enable_ai=True)
        batch_processor = BatchProcessor()
        
        # Test files (create duplicates to test deduplication)
        test_files = ['test_image.png']
        if os.path.exists('test_image_duplicate1.png'):
            test_files.append('test_image_duplicate1.png')
        
        print(f"\n📁 Processing {len(test_files)} files...")
        print("Progress will show: Starting → Converting → Completed\n")
        
        # Process batch with detailed progress
        result = batch_processor.process_batch(
            test_files,
            output_folder,
            converter,
            detailed_progress_callback
        )
        
        print(f"\n✅ Batch Processing Complete!")
        print(f"📊 Results:")
        print(f"  • Successful: {len(result.successful_files)} files")
        print(f"  • Failed: {len(result.failed_files)} files")
        print(f"  • Skipped: {len(result.skipped_files)} files")
        print(f"  • Total size: {result.total_size_mb:.2f} MB")
        
        if result.failed_files:
            print(f"\n❌ Failed files:")
            for file_path, error in result.failed_files:
                print(f"  • {os.path.basename(file_path)}: {error}")
        
        print(f"\n🎉 The progress bar now provides real-time feedback!")
        print("Users will see exactly what's happening at each stage.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_progress_reporting()