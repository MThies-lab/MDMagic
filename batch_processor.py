#!/usr/bin/env python3
"""
Batch processor for MarkdownMagic - handles multiple file conversions with size limits
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class BatchResult:
    """Result of a batch conversion operation"""
    successful_files: List[str]
    failed_files: List[Tuple[str, str]]  # (filename, error_message)
    total_size_mb: float
    total_files: int
    skipped_files: List[Tuple[str, str]]  # (filename, reason)

class BatchProcessor:
    """
    Handles batch processing of multiple documents with size and format validation
    """
    
    def __init__(self, max_batch_size_mb: float = 250.0):
        """
        Initialize BatchProcessor
        
        Args:
            max_batch_size_mb: Maximum total file size for a batch in MB
        """
        self.max_batch_size_mb = max_batch_size_mb
        self.supported_extensions = {'.txt', '.pdf', '.docx', '.odt', '.rtf', '.html', '.htm', '.xlsx', '.xls'}
    
    def validate_batch(self, file_paths: List[str]) -> Tuple[List[str], List[Tuple[str, str]], float]:
        """
        Validate a batch of files for processing
        
        Args:
            file_paths: List of file paths to validate
            
        Returns:
            Tuple[List[str], List[Tuple[str, str]], float]: 
            (valid_files, invalid_files_with_reasons, total_size_mb)
        """
        valid_files = []
        invalid_files = []
        total_size_bytes = 0
        
        for file_path in file_paths:
            file_path = str(file_path).strip()
            
            # Check if file exists
            if not os.path.exists(file_path):
                invalid_files.append((file_path, "File not found"))
                continue
            
            # Check if it's a file (not directory)
            if not os.path.isfile(file_path):
                invalid_files.append((file_path, "Not a file"))
                continue
            
            # Check file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self.supported_extensions:
                invalid_files.append((file_path, f"Unsupported format: {file_ext}"))
                continue
            
            # Check file size
            try:
                file_size = os.path.getsize(file_path)
                
                # Check if adding this file would exceed the batch limit
                if (total_size_bytes + file_size) > (self.max_batch_size_mb * 1024 * 1024):
                    invalid_files.append((file_path, f"Would exceed {self.max_batch_size_mb}MB batch limit"))
                    continue
                
                # File is valid
                valid_files.append(file_path)
                total_size_bytes += file_size
                
            except OSError as e:
                invalid_files.append((file_path, f"Cannot read file size: {e}"))
                continue
        
        total_size_mb = total_size_bytes / (1024 * 1024)
        return valid_files, invalid_files, total_size_mb
    
    def process_batch(self, file_paths: List[str], output_folder: str, 
                     converter, progress_callback: Optional[callable] = None) -> BatchResult:
        """
        Process a batch of files
        
        Args:
            file_paths: List of file paths to convert
            output_folder: Destination folder for converted files
            converter: DocumentConverter instance
            progress_callback: Optional callback function for progress updates
            
        Returns:
            BatchResult: Results of the batch processing
        """
        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Validate the batch
        valid_files, invalid_files, total_size_mb = self.validate_batch(file_paths)
        
        successful_files = []
        failed_files = []
        skipped_files = invalid_files.copy()  # Files that were skipped during validation
        
        total_files = len(valid_files)
        
        # Process each valid file
        for i, file_path in enumerate(valid_files):
            try:
                # Generate output filename
                input_file = Path(file_path)
                output_filename = f"{input_file.stem}.md"
                output_path = os.path.join(output_folder, output_filename)
                
                # Handle filename conflicts
                counter = 1
                original_output_path = output_path
                while os.path.exists(output_path):
                    output_filename = f"{input_file.stem}_{counter}.md"
                    output_path = os.path.join(output_folder, output_filename)
                    counter += 1
                
                # Call progress callback if provided
                if progress_callback:
                    progress_callback(i + 1, total_files, file_path)
                
                # Convert the file
                result_path = converter.convert_to_markdown(file_path, output_path)
                successful_files.append(result_path)
                
                print(f"✓ Converted: {input_file.name} → {Path(result_path).name}")
                
            except Exception as e:
                failed_files.append((file_path, str(e)))
                print(f"✗ Failed: {Path(file_path).name} - {e}")
        
        return BatchResult(
            successful_files=successful_files,
            failed_files=failed_files,
            total_size_mb=total_size_mb,
            total_files=len(file_paths),
            skipped_files=skipped_files
        )
    
    def collect_files_from_folder(self, folder_path: str, recursive: bool = False) -> List[str]:
        """
        Collect all supported files from a folder
        
        Args:
            folder_path: Path to the folder to scan
            recursive: Whether to scan subfolders recursively
            
        Returns:
            List[str]: List of file paths found
        """
        collected_files = []
        folder_path = Path(folder_path)
        
        if not folder_path.exists() or not folder_path.is_dir():
            raise ValueError(f"Invalid folder path: {folder_path}")
        
        # Choose the appropriate scan method
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        # Scan for files
        for file_path in folder_path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                collected_files.append(str(file_path))
        
        return sorted(collected_files)
    
    def get_batch_summary(self, file_paths: List[str]) -> Dict[str, any]:
        """
        Get a summary of a potential batch
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Dict: Summary information about the batch
        """
        valid_files, invalid_files, total_size_mb = self.validate_batch(file_paths)
        
        # Count files by type
        file_types = {}
        for file_path in valid_files:
            ext = Path(file_path).suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            'total_files': len(file_paths),
            'valid_files': len(valid_files),
            'invalid_files': len(invalid_files),
            'total_size_mb': total_size_mb,
            'within_size_limit': total_size_mb <= self.max_batch_size_mb,
            'file_types': file_types,
            'invalid_details': invalid_files
        }
    
    def print_batch_summary(self, file_paths: List[str]) -> None:
        """
        Print a formatted summary of the batch
        
        Args:
            file_paths: List of file paths to analyze
        """
        summary = self.get_batch_summary(file_paths)
        
        print("=== Batch Summary ===")
        print(f"Total files: {summary['total_files']}")
        print(f"Valid files: {summary['valid_files']}")
        print(f"Invalid files: {summary['invalid_files']}")
        print(f"Total size: {summary['total_size_mb']:.2f} MB")
        print(f"Size limit: {self.max_batch_size_mb} MB")
        
        if summary['within_size_limit']:
            print("✓ Within size limit")
        else:
            print("✗ Exceeds size limit")
        
        if summary['file_types']:
            print("\nFile types:")
            for ext, count in summary['file_types'].items():
                print(f"  {ext}: {count} files")
        
        if summary['invalid_details']:
            print(f"\nInvalid files:")
            for file_path, reason in summary['invalid_details']:
                print(f"  ✗ {Path(file_path).name}: {reason}")
        
        print("=" * 20)