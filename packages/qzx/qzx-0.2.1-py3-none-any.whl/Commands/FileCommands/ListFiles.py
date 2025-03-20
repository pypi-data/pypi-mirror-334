#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ListFiles Command - Lists files in a directory with support for wildcards and recursive searching
"""

import os
import glob
import time
import re
from pathlib import Path
from Core.command_base import CommandBase

class ListFilesCommand(CommandBase):
    """
    Command to list files in a directory with support for wildcards and recursive searching
    """
    
    name = "listFiles"
    description = "Lists files in a directory with support for wildcards and recursive searching"
    category = "file"
    
    parameters = [
        {
            'name': 'directory_path',
            'description': 'Path to the directory to list files from',
            'required': False,
            'default': '.'
        },
        {
            'name': 'pattern',
            'description': 'File pattern to filter by (e.g., "*.txt", "doc*.pdf")',
            'required': False,
            'default': '*'
        },
        {
            'name': 'recursive',
            'description': 'Recursion level: none by default, -r/--recursive for unlimited depth, -rN/--recursiveN for N levels deep',
            'required': False,
            'default': None
        }
    ]
    
    examples = [
        {
            'command': 'qzx listFiles',
            'description': 'List all files in the current directory'
        },
        {
            'command': 'qzx listFiles C:\\Documents',
            'description': 'List all files in the C:\\Documents directory (Windows)'
        },
        {
            'command': 'qzx listFiles /home/user/documents',
            'description': 'List all files in the /home/user/documents directory (Linux/Mac)'
        },
        {
            'command': 'qzx listFiles . "*.py"',
            'description': 'List all Python files in the current directory'
        },
        {
            'command': 'qzx listFiles src "*.js" -r',
            'description': 'List all JavaScript files in the src directory and all its subdirectories'
        },
        {
            'command': 'qzx listFiles src "*.js" -r2',
            'description': 'List all JavaScript files in the src directory and up to 2 levels of subdirectories'
        }
    ]
    
    def _parse_recursive_parameter(self, recursive_param):
        """
        Parse the recursive parameter into a depth value
        
        Args:
            recursive_param: The raw recursive parameter (string or bool)
            
        Returns:
            int or None: Maximum recursion depth (None for unlimited, 0 for none)
        """
        try:
            # Default is no recursion (0) if parameter is None
            if recursive_param is None:
                return 0
                
            # If it's a boolean or convertible to boolean
            if isinstance(recursive_param, bool):
                return None if recursive_param else 0
                
            # If it's directly an integer
            if isinstance(recursive_param, int):
                return max(0, recursive_param)  # Ensure it's not negative
                
            # If it's a string, try different formats
            if isinstance(recursive_param, str):
                # Convert to lowercase for standardization
                recursive_param = recursive_param.lower()
                
                # Boolean strings
                if recursive_param in ('true', 'yes', 'y', '1'):
                    return None
                elif recursive_param in ('false', 'no', 'n', '0'):
                    return 0
                    
                # Try to convert directly to integer
                try:
                    depth = int(recursive_param)
                    return max(0, depth)  # Ensure it's not negative
                except ValueError:
                    pass
                    
                # Parse -r or --recursive format
                if recursive_param == '-r' or recursive_param == '--recursive':
                    return None  # Unlimited recursion
                    
                # Try to parse -rN format (e.g. -r3)
                r_depth_match = re.match(r'^-r(\d+)$', recursive_param)
                if r_depth_match:
                    return int(r_depth_match.group(1))
                
                # Try to parse --recursiveN format (e.g. --recursive3)
                recursive_match = re.match(r'^--recursive(\d+)$', recursive_param)
                if recursive_match:
                    return int(recursive_match.group(1))
            
            # If it doesn't match any known format, use the default (no recursion)
            return 0
        except Exception:
            # In case of any exception, return the default
            return 0
    
    def _find_files(self, directory_path, pattern, recursive=None):
        """
        Find files matching the given pattern in the specified directory
        
        Args:
            directory_path (str): Directory to search in
            pattern (str): File pattern to match
            recursive: Recursion parameter (None/0 for none, -r/--recursive or None for unlimited, -rN/--recursiveN for N levels)
            
        Returns:
            list: Matching file paths
        """
        # Parse the recursive parameter to get the max depth
        max_depth = self._parse_recursive_parameter(recursive)
        
        # Handle Windows paths
        directory_path = directory_path.replace('\\', '/')
        
        # Ensure directory exists
        if not os.path.exists(directory_path):
            return []
            
        if not os.path.isdir(directory_path):
            return []
            
        # Non-recursive search (max_depth = 0)
        if max_depth == 0:
            search_pattern = os.path.join(directory_path, pattern)
            matching_files = glob.glob(search_pattern)
            return [f for f in matching_files if os.path.isfile(f)]
            
        # Unlimited recursive search (max_depth = None)
        if max_depth is None:
            # Construct search pattern for unlimited recursion
            search_pattern = os.path.join(directory_path, '**', pattern)
            matching_files = glob.glob(search_pattern, recursive=True)
            return [f for f in matching_files if os.path.isfile(f)]
            
        # Limited depth recursive search (max_depth > 0)
        # For limited depth, we need to use os.walk with a depth limit
        matching_files = []
        for root, _, files in os.walk(directory_path):
            # Calculate current depth
            rel_path = os.path.relpath(root, directory_path)
            current_depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
            
            # Skip if we've exceeded the max depth
            if current_depth > max_depth:
                continue
                
            # Check for matching files at this level
            for file in files:
                if glob.fnmatch.fnmatch(file, pattern):
                    matching_files.append(os.path.join(root, file))
                    
        return matching_files
            
    def execute(self, directory_path=".", pattern="*", recursive=None):
        """
        Lists files in a directory with support for wildcards and recursive searching
        
        Args:
            directory_path (str): Path to the directory to list files from
            pattern (str): File pattern to filter by (e.g., "*.txt", "doc*.pdf")
            recursive: Recursion level: none by default, -r/--recursive for unlimited, -rN/--recursiveN for N levels
            
        Returns:
            Dictionary with the list of files and metadata
        """
        try:
            # Normalize parameters
            if directory_path is None:
                directory_path = "."
            
            if pattern is None:
                pattern = "*"

            # Debug output to see what parameters are being received
            print(f"DEBUG ListFiles - Params: dir={directory_path}, pattern={pattern}, recursive={recursive}")
            
            # Find matching files
            files = self._find_files(directory_path, pattern, recursive)
            
            # Get the parsed recursion depth for the result message
            recursion_depth = self._parse_recursive_parameter(recursive)
            recursion_message = ""
            if recursion_depth is None:
                recursion_message = " (including all subdirectories)"
            elif recursion_depth > 0:
                recursion_message = f" (including subdirectories up to {recursion_depth} level{'s' if recursion_depth > 1 else ''})"
            
            if not files:
                return {
                    "success": True,
                    "message": f"No files found matching pattern '{pattern}' in {directory_path}" + recursion_message,
                    "files": []
                }

            # Prepare file list with metadata
            file_list = []
            total_size = 0
            
            for file_path in files:
                try:
                    file_stat = os.stat(file_path)
                    size = file_stat.st_size
                    mod_time = file_stat.st_mtime
                    
                    # Convert to relative path if requested path was relative
                    if not os.path.isabs(directory_path):
                        rel_path = os.path.relpath(file_path)
                    else:
                        rel_path = file_path
                    
                    file_list.append({
                        "path": rel_path,
                        "size": size,
                        "size_readable": self._format_size(size),
                        "modified": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
                    })
                    
                    total_size += size
                except Exception as e:
                    # Skip files with access issues
                    continue
            
            # Sort files by path
            file_list.sort(key=lambda x: x["path"])
            
            # Get a descriptive recursion string for the result
            if recursion_depth is None:
                recursion_info = "unlimited"
            elif recursion_depth == 0:
                recursion_info = "none"
            else:
                recursion_info = str(recursion_depth)
            
            return {
                "success": True,
                "directory": os.path.abspath(directory_path),
                "pattern": pattern,
                "recursive": recursion_info,
                "file_count": len(file_list),
                "total_size": total_size,
                "total_size_readable": self._format_size(total_size),
                "files": file_list
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def _format_size(self, size_bytes):
        """Format a size in bytes to a human-readable string"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB" 