#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FindLargeFiles Command - Searches for files matching a pattern with size filter
"""

import os
import fnmatch
import glob
import re
import time
from datetime import datetime
from pathlib import Path
from Core.command_base import CommandBase

class FindLargeFilesCommand(CommandBase):
    """
    Command to find files of specified type exceeding a minimum size
    """
    
    name = "findLargeFiles"
    description = "Searches for files with specific extensions that exceed a given size"
    category = "file"
    
    parameters = [
        {
            'name': 'directory',
            'description': 'Base directory to start the search from',
            'required': True
        },
        {
            'name': 'extension',
            'description': 'File extension to filter by (e.g., "*.pas", "*.txt")',
            'required': True
        },
        {
            'name': 'min_size',
            'description': 'Minimum file size in bytes',
            'required': True
        },
        {
            'name': 'recursive',
            'description': 'Recursion level: -r/--recursive for unlimited depth, -rN/--recursiveN for N levels deep',
            'required': False,
            'default': '-r'
        },
        {
            'name': 'sort_by',
            'description': 'Sort results by: "name", "size", "date"',
            'required': False,
            'default': 'size'
        }
    ]
    
    examples = [
        {
            'command': 'qzx findLargeFiles . *.pas 300',
            'description': 'Find all .pas files in current directory larger than 300 bytes'
        },
        {
            'command': 'qzx findLargeFiles src *.py 1024 true',
            'description': 'Find all .py files in src directory and subdirectories larger than 1KB'
        },
        {
            'command': 'qzx findLargeFiles project *.js 5000 false name',
            'description': 'Find all .js files (non-recursive) larger than 5KB, sorted by name'
        }
    ]
    
    def _parse_recursive_parameter(self, recursive_param):
        """
        Parse the recursive parameter into a depth value
        
        Args:
            recursive_param: The raw recursive parameter (string)
            
        Returns:
            int or None: Maximum recursion depth (None for unlimited, 0 for none)
        """
        # Default is unlimited recursion (None) if parameter is None
        if recursive_param is None:
            return None
            
        # Only accept string parameters with the new format
        if isinstance(recursive_param, str):
            # New format: -r or --recursive for unlimited recursion
            if recursive_param in ('-r', '--recursive'):
                return None
                
            # New format: -rN or --recursiveN for N levels of recursion
            r_match = re.match(r'^-r(\d+)$', recursive_param)
            if r_match:
                return int(r_match.group(1))
                
            recursive_match = re.match(r'^--recursive(\d+)$', recursive_param)
            if recursive_match:
                return int(recursive_match.group(1))
                
        # Default to unlimited recursion if the format is not recognized
        return None
    
    def _parse_size(self, size_str):
        """
        Parse a size string like '10MB' into bytes
        
        Args:
            size_str (str): Size string (e.g., '10MB', '1.5GB', '500KB')
            
        Returns:
            int: Size in bytes
            
        Raises:
            ValueError: If the format is invalid
        """
        if not size_str:
            return 0
            
        # If it's already a number, return it
        if isinstance(size_str, (int, float)):
            return int(size_str)
            
        # Parse string format
        size_str = str(size_str).strip().upper()
        
        # Handle different formats
        if size_str.endswith('B'):
            if size_str.endswith('KB'):
                multiplier = 1024
                size_value = float(size_str[:-2])
            elif size_str.endswith('MB'):
                multiplier = 1024 * 1024
                size_value = float(size_str[:-2])
            elif size_str.endswith('GB'):
                multiplier = 1024 * 1024 * 1024
                size_value = float(size_str[:-2])
            elif size_str.endswith('TB'):
                multiplier = 1024 * 1024 * 1024 * 1024
                size_value = float(size_str[:-2])
            else:  # Just bytes
                multiplier = 1
                size_value = float(size_str[:-1])
        else:
            # Try to parse as a plain number
            try:
                return int(size_str)
            except ValueError:
                raise ValueError(f"Invalid size format: {size_str}. Use formats like '10MB', '1.5GB', etc.")
                
        return int(size_value * multiplier)
    
    def _format_size(self, size_bytes):
        """
        Format a size in bytes to a human-readable string
        
        Args:
            size_bytes (int): Size in bytes
            
        Returns:
            str: Formatted size string
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def execute(self, directory, extension, min_size, recursive=None, sort_by='size'):
        """
        Find large files in a directory matching the given criteria
        
        Args:
            directory (str): Directory to search in
            extension (str): File extension to filter by (e.g., 'jpg' or '.jpg')
            min_size (str): Minimum file size (e.g., '1MB', '500KB')
            recursive: Recursion level: none by default, -r/--recursive for unlimited, -rN/--recursiveN for N levels
            sort_by (str): Sort criteria ('size', 'name', or 'date')
            
        Returns:
            Dictionary with search results
        """
        try:
            # Check that the directory exists
            if not os.path.exists(directory):
                return {
                    "success": False,
                    "error": f"Directory not found: {directory}"
                }
                
            if not os.path.isdir(directory):
                return {
                    "success": False,
                    "error": f"Not a directory: {directory}"
                }
            
            # Parse minimum size
            try:
                min_size_bytes = self._parse_size(min_size)
            except ValueError as e:
                return {
                    "success": False,
                    "error": f"Invalid minimum size format: {min_size}. {str(e)}"
                }
            
            # Parse recursion parameter
            recursion_depth = self._parse_recursive_parameter(recursive)
            
            # Validate sort_by
            valid_sort_options = ['name', 'size', 'date']
            if sort_by.lower() not in valid_sort_options:
                return {
                    "success": False,
                    "error": f"Invalid sort_by option: '{sort_by}'. Must be one of: {', '.join(valid_sort_options)}"
                }
            
            # Make sure extension has proper format (*.ext)
            if not extension.startswith('*'):
                extension = f'*{extension}' if extension.startswith('.') else f'*.{extension}'
            
            # Find files
            matching_files = []
            
            # Get a descriptive recursion string for the result message
            recursion_message = ""
            if recursion_depth is None:
                recursion_message = " (including all subdirectories)"
            elif recursion_depth > 0:
                recursion_message = f" (including subdirectories up to {recursion_depth} level{'s' if recursion_depth > 1 else ''})"
            
            # Process based on recursion depth
            if recursion_depth == 0:
                # Non-recursive search
                for file in glob.glob(os.path.join(directory, extension)):
                    if os.path.isfile(file):
                        file_size = os.path.getsize(file)
                        if file_size >= min_size_bytes:
                            matching_files.append({
                                "path": file,
                                "size": file_size,
                                "size_readable": self._format_size(file_size),
                                "modified": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file)))
                            })
            else:
                # Recursive search with optional depth limit
                for root, _, files in os.walk(directory):
                    # Calculate current depth relative to directory
                    rel_path = os.path.relpath(root, directory)
                    current_depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
                    
                    # Skip if depth exceeds the limit and not doing unlimited recursion
                    if recursion_depth is not None and current_depth > recursion_depth:
                        continue
                    
                    # Process files at this level
                    for file in files:
                        if fnmatch.fnmatch(file, extension):
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path)
                            if file_size >= min_size_bytes:
                                matching_files.append({
                                    "path": file_path,
                                    "size": file_size,
                                    "size_readable": self._format_size(file_size),
                                    "modified": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
                                })
            
            # Sort results
            if sort_by.lower() == 'name':
                matching_files.sort(key=lambda x: x["path"])
            elif sort_by.lower() == 'size':
                matching_files.sort(key=lambda x: x["size"], reverse=True)
            elif sort_by.lower() == 'date':
                matching_files.sort(key=lambda x: os.path.getmtime(x["path"]), reverse=True)
            
            # Get a descriptive recursion string for the result
            recursion_info = "unlimited"
            if recursion_depth == 0:
                recursion_info = "none"
            elif recursion_depth is not None:
                recursion_info = str(recursion_depth)
                
            # Prepare result
            total_size = sum(f["size"] for f in matching_files)
            result = {
                "success": True,
                "directory": os.path.abspath(directory),
                "extension": extension,
                "min_size": min_size,
                "min_size_bytes": min_size_bytes,
                "recursive": recursion_info,
                "sort_by": sort_by,
                "files_found": len(matching_files),
                "total_size": total_size,
                "total_size_readable": self._format_size(total_size),
                "files": matching_files
            }
            
            return result
        except Exception as e:
            return {
                "success": False,
                "directory": directory,
                "extension": extension,
                "min_size": min_size,
                "error": str(e)
            }
    
    def _format_bytes(self, size):
        """
        Format bytes to human-readable size
        
        Args:
            size (int): Size in bytes
            
        Returns:
            str: Human-readable size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024.0 or unit == 'PB':
                break
            size /= 1024.0
        return f"{size:.2f} {unit}" 