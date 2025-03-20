#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MoveFile Command - Moves or renames a file or directory
"""

import os
import shutil
from Core.command_base import CommandBase

class MoveFileCommand(CommandBase):
    """
    Command to move or rename a file or directory
    """
    
    name = "moveFile"
    description = "Moves or renames a file or directory from source to destination"
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
            'command': 'qzx moveFile source.txt destination.txt',
            'description': 'Move a file to another (or rename it)'
        },
        {
            'command': 'qzx moveFile myfile.txt archive/myfile.txt',
            'description': 'Move a file to a directory'
        },
        {
            'command': 'qzx moveFile sourcedir destinationdir true',
            'description': 'Move a directory and overwrite if exists'
        }
    ]
    
    def execute(self, source, destination, force=False):
        """
        Moves or renames a file or directory
        
        Args:
            source (str): Path to the source file or directory
            destination (str): Path to the destination file or directory
            force (bool, optional): Whether to overwrite the destination if it exists
            
        Returns:
            Operation result
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
            
            # Determine the type of operation (file or directory)
            source_is_dir = os.path.isdir(source)
            
            # Prepare the result
            result = {
                "source": os.path.abspath(source),
                "destination": os.path.abspath(destination),
                "type": "directory" if source_is_dir else "file",
                "force": force,
                "success": True
            }
            
            # If destination exists and force=True, remove it first
            if os.path.exists(destination) and force:
                if os.path.isdir(destination):
                    shutil.rmtree(destination)
                else:
                    os.remove(destination)
            
            # Move the file or directory
            shutil.move(source, destination)
            
            result["message"] = f"'{source}' moved to '{destination}'"
            
            return result
        except Exception as e:
            return {
                "success": False,
                "source": source,
                "destination": destination,
                "error": str(e)
            } 