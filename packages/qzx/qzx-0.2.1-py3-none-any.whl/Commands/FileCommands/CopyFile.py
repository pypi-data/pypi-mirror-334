#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CopyFile Command - Copies a file or directory
"""

import os
import shutil
from Core.command_base import CommandBase

class CopyFileCommand(CommandBase):
    """
    Command to copy a file or directory
    """
    
    name = "copyFile"
    description = "Copies a file or directory from source to destination"
    category = "file"
    
    parameters = [
        {
            'name': 'source',
            'description': 'Path to the source file or directory',
            'required': True
        },
        {
            'name': 'destination',
            'description': 'Path to the destination file or directory',
            'required': True
        },
        {
            'name': 'force',
            'description': 'Whether to overwrite the destination if it exists',
            'required': False,
            'default': False
        }
    ]
    
    examples = [
        {
            'command': 'qzx copyFile source.txt destination.txt',
            'description': 'Copy a file to another file'
        },
        {
            'command': 'qzx copyFile myfile.txt backup/myfile.txt',
            'description': 'Copy a file to a directory'
        },
        {
            'command': 'qzx copyFile sourcedir destinationdir true',
            'description': 'Copy a directory recursively and overwrite if exists'
        }
    ]
    
    def execute(self, source, destination, force=False):
        """
        Copies a file or directory
        
        Args:
            source (str): Path to the source file or directory
            destination (str): Path to the destination file or directory
            force (bool, optional): Whether to overwrite the destination if it exists
            
        Returns:
            Success message or error
        """
        try:
            # Convert force to boolean if it's a string
            if isinstance(force, str):
                force = force.lower() in ('true', 'yes', 'y', '1')
            
            # Check if source exists
            if not os.path.exists(source):
                return {
                    "success": False,
                    "error": f"Source '{source}' does not exist"
                }
            
            # Check if destination exists and if we should overwrite
            if os.path.exists(destination) and not force:
                return {
                    "success": False,
                    "error": f"Destination '{destination}' already exists. Use force=True to overwrite."
                }
            
            # Create destination directory if it doesn't exist
            dest_dir = os.path.dirname(destination)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            # Determine the type of copy (file or directory)
            source_is_dir = os.path.isdir(source)
            
            # Perform the copy
            result = {
                "source": os.path.abspath(source),
                "destination": os.path.abspath(destination),
                "type": "directory" if source_is_dir else "file",
                "force": force,
                "success": True
            }
            
            if source_is_dir:
                # Copy directory recursively
                if os.path.exists(destination) and force:
                    # If destination exists and force=True, remove it first
                    shutil.rmtree(destination, ignore_errors=True)
                
                shutil.copytree(source, destination)
                result["message"] = f"Directory '{source}' copied to '{destination}'"
            else:
                # Copy a single file
                shutil.copy2(source, destination)
                
                # Get file information
                src_size = os.path.getsize(source)
                dst_size = os.path.getsize(destination)
                
                result["message"] = f"File '{source}' copied to '{destination}'"
                result["file_size"] = src_size
                result["file_size_readable"] = self._format_bytes(src_size)
                
                # Verify that the size matches
                if src_size != dst_size:
                    result["warning"] = f"Source file size ({src_size} bytes) and destination file size ({dst_size} bytes) do not match"
            
            return result
        except Exception as e:
            return {
                "success": False,
                "source": source,
                "destination": destination,
                "error": str(e)
            }
    
    def _format_bytes(self, bytes_value):
        """
        Format bytes to human-readable format
        
        Args:
            bytes_value (int): Bytes to format
            
        Returns:
            str: Formatted string with appropriate unit
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024 or unit == 'TB':
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024 