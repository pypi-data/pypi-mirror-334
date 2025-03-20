#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CountLinesInFile Command - Counts the number of lines in files with support for wildcards and recursive searching
"""

import os
import glob
import fnmatch
import re
from pathlib import Path
from collections import defaultdict
from Core.command_base import CommandBase

class CountLinesInFileCommand(CommandBase):
    """
    Command to count the number of lines in files with support for wildcards and recursive searching
    """
    
    name = "countLinesInFile"
    description = "Counts the number of lines in files with support for wildcards and recursive searching"
    category = "file"
    
    parameters = [
        {
            'name': 'file_path',
            'description': 'Path to the file(s) to count lines in. Supports wildcards like "*.py"',
            'required': True
        },
        {
            'name': 'recursive',
            'description': 'Recursion level: -r/--recursive for unlimited depth, -rN/--recursiveN for N levels deep',
            'required': False,
            'default': None
        },
        {
            'name': 'ignore_empty',
            'description': 'Whether to ignore empty lines when counting',
            'required': False,
            'default': False
        }
    ]
    
    examples = [
        {
            'command': 'qzx countLinesInFile "script.py"',
            'description': 'Count the number of lines in a Python script'
        },
        {
            'command': 'qzx countLinesInFile "data/logs.txt"',
            'description': 'Count the number of lines in a log file'
        },
        {
            'command': 'qzx countLinesInFile "*.py"',
            'description': 'Count the number of lines in all Python files in the current directory'
        },
        {
            'command': 'qzx countLinesInFile "src/**/*.js" true',
            'description': 'Count the number of lines in all JavaScript files in the src directory and its subdirectories'
        },
        {
            'command': 'qzx countLinesInFile "*.txt" false true',
            'description': 'Count the number of non-empty lines in all text files in the current directory'
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
        # Default is no recursion (0) if parameter is None
        if recursive_param is None:
            return 0
            
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
                
        # Default to no recursion if the format is not recognized
        return 0
    
    def _find_files(self, file_path_pattern, recursive=None):
        """
        Find files matching the given pattern, with optional recursive search
        
        Args:
            file_path_pattern (str): File path pattern (may include wildcards)
            recursive: Recursion parameter (None/0 for none, -r/--recursive or None for unlimited, -rN/--recursiveN for N levels)
            
        Returns:
            list: List of file paths matching the pattern
        """
        # Parse the recursive parameter to get the max depth
        max_depth = self._parse_recursive_parameter(recursive)
        
        # Handle Windows paths
        file_path_pattern = file_path_pattern.replace('\\', '/')
        
        if not any(char in file_path_pattern for char in '*?[]'):
            # No wildcard - direct file or directory
            if os.path.isfile(file_path_pattern):
                return [file_path_pattern]
            elif os.path.isdir(file_path_pattern):
                # If it's a directory, handle based on recursion depth
                if max_depth == 0:
                    # Just return files in the top directory
                    return [os.path.join(file_path_pattern, f) for f in os.listdir(file_path_pattern) 
                            if os.path.isfile(os.path.join(file_path_pattern, f))]
                elif max_depth is None:
                    # Get all files recursively with no depth limit
                    result = []
                    for root, _, files in os.walk(file_path_pattern):
                        for file in files:
                            result.append(os.path.join(root, file))
                    return result
                else:
                    # Get files with depth limit
                    result = []
                    for root, _, files in os.walk(file_path_pattern):
                        # Calculate current depth
                        rel_path = os.path.relpath(root, file_path_pattern)
                        current_depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
                        
                        # Skip if we've exceeded the max depth
                        if current_depth > max_depth:
                            continue
                            
                        # Add files at this level
                        for file in files:
                            result.append(os.path.join(root, file))
                    return result
            else:
                return []
        
        # Handle glob patterns based on recursion depth
        if max_depth == 0:
            # Non-recursive glob
            return glob.glob(file_path_pattern)
        elif max_depth is None:
            # Unlimited recursive glob
            if '**' in file_path_pattern:
                # Pattern already has ** for recursive matching
                return glob.glob(file_path_pattern, recursive=True)
            else:
                # Add ** to the pattern for recursive matching
                dir_part = os.path.dirname(file_path_pattern)
                if dir_part:
                    # Replace the directory part with **/ for recursive search
                    file_name_part = os.path.basename(file_path_pattern)
                    recursive_pattern = os.path.join(dir_part, '**', file_name_part)
                    return glob.glob(recursive_pattern, recursive=True)
                else:
                    # If no directory part, just prepend **/ to the pattern
                    return glob.glob(f'**/{file_path_pattern}', recursive=True)
        else:
            # Limited depth recursive search using os.walk
            result = []
            dir_part = os.path.dirname(file_path_pattern) or '.'
            file_pattern = os.path.basename(file_path_pattern)
            
            for root, _, files in os.walk(dir_part):
                # Calculate current depth
                rel_path = os.path.relpath(root, dir_part)
                current_depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
                
                # Skip if we've exceeded the max depth
                if current_depth > max_depth:
                    continue
                    
                # Check for matching files at this level
                for file in files:
                    if fnmatch.fnmatch(file, file_pattern):
                        result.append(os.path.join(root, file))
                        
            return result
    
    def _count_lines(self, file_path, ignore_empty=False):
        """
        Count lines in a single file
        
        Args:
            file_path (str): Path to the file
            ignore_empty (bool): Whether to ignore empty lines
            
        Returns:
            tuple: (line_count, non_empty_lines, success, error_message)
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                if ignore_empty:
                    lines = [line for line in file if line.strip()]
                    return (len(lines), len(lines), True, None)
                else:
                    lines = file.readlines()
                    non_empty = sum(1 for line in lines if line.strip())
                    return (len(lines), non_empty, True, None)
        except Exception as e:
            return (0, 0, False, str(e))
    
    def execute(self, file_path, recursive=None, ignore_empty=False):
        """
        Counts the number of lines in files with support for wildcards and recursive searching
        
        Args:
            file_path: Path to the file(s) to count lines in. Supports wildcards like "*.py"
            recursive: Recursion level: none by default, -r/--recursive for unlimited, -rN/--recursiveN for N levels
            ignore_empty: Whether to ignore empty lines when counting
            
        Returns:
            Dictionary with line count results or error message
        """
        try:
            # Parse recursion parameter
            recursion_depth = self._parse_recursive_parameter(recursive)
            
            # Convert ignore_empty parameter if it's a string
            if isinstance(ignore_empty, str):
                ignore_empty = ignore_empty.lower() in ('true', 'yes', 'y', '1')
            
            # Find matching files
            matching_files = self._find_files(file_path, recursive)
            
            # Get a descriptive recursion string for the result message
            recursion_message = ""
            if recursion_depth is None:
                recursion_message = " (including all subdirectories)"
            elif recursion_depth > 0:
                recursion_message = f" (including subdirectories up to {recursion_depth} level{'s' if recursion_depth > 1 else ''})"
            
            if not matching_files:
                return {
                    "success": True,
                    "message": f"No files found matching pattern '{file_path}'" + recursion_message,
                    "files": []
                }
            
            # Process each file
            total_lines = 0
            total_non_empty = 0
            file_results = []
            failed_files = []
            
            for file_path in matching_files:
                line_count, non_empty, success, error = self._count_lines(file_path, ignore_empty)
                
                if success:
                    # Add to totals
                    total_lines += line_count
                    total_non_empty += non_empty
                    
                    # Add to results
                    file_results.append({
                        "file": file_path,
                        "line_count": line_count if not ignore_empty else non_empty,
                        "non_empty_lines": non_empty,
                        "empty_lines": line_count - non_empty
                    })
                else:
                    failed_files.append({
                        "file": file_path,
                        "error": error
                    })
            
            # Group results by file type
            extension_stats = defaultdict(int)
            for result in file_results:
                _, ext = os.path.splitext(result["file"])
                ext = ext.lower() if ext else "no extension"
                extension_stats[ext] += result["line_count"]
            
            # Build the response
            result = {
                "success": True,
                "file_pattern": file_path,
                "recursive": recursion_depth,
                "ignore_empty": ignore_empty,
                "files_analyzed": len(file_results),
                "files_failed": len(failed_files),
                "total_lines": total_lines if not ignore_empty else total_non_empty,
                "total_non_empty_lines": total_non_empty,
                "total_empty_lines": total_lines - total_non_empty if not ignore_empty else 0,
                "files": file_results,
                "failed_files": failed_files,
                "extension_stats": dict(extension_stats)
            }
            
            # Add summary message
            if len(matching_files) == 1:
                # Single file
                message = f"File {matching_files[0]} has {result['total_lines']} lines"
                if not ignore_empty:
                    message += f" ({result['total_non_empty_lines']} non-empty, {result['total_empty_lines']} empty)"
            else:
                # Multiple files
                message = f"Analyzed {len(file_results)} files with {result['total_lines']} total lines"
                if not ignore_empty:
                    message += f" ({result['total_non_empty_lines']} non-empty, {result['total_empty_lines']} empty)"
                if failed_files:
                    message += f". {len(failed_files)} files could not be analyzed."
                    
            result["message"] = message
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error counting lines: {str(e)}"
            } 