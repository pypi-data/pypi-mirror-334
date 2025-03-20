#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ChangePermissions Command - Changes file or directory permissions
"""

import os
import platform
import stat
from Core.command_base import CommandBase

class ChangePermissionsCommand(CommandBase):
    """
    Command to change file or directory permissions (similar to chmod)
    """
    
    name = "changePermissions"
    description = "Changes permissions of a file or directory"
    category = "file"
    
    parameters = [
        {
            'name': 'path',
            'description': 'Path to the file or directory',
            'required': True
        },
        {
            'name': 'mode',
            'description': 'Permission mode in octal (e.g., 755) or string format (e.g., "a+x")',
            'required': True
        },
        {
            'name': 'recursive',
            'description': 'Whether to apply permissions recursively to directories',
            'required': False,
            'default': False
        }
    ]
    
    examples = [
        {
            'command': 'qzx changePermissions myfile.txt 644',
            'description': 'Change file permissions to 644 (rw-r--r--)'
        },
        {
            'command': 'qzx changePermissions myscript.sh "a+x"',
            'description': 'Make a script executable for all users'
        },
        {
            'command': 'qzx changePermissions mydir 755 true',
            'description': 'Change directory permissions recursively'
        }
    ]
    
    def execute(self, path, mode, recursive=False):
        """
        Changes permissions of a file or directory
        
        Args:
            path (str): Path to the file or directory
            mode (str/int): Permission mode in octal (e.g., 755) or string format (e.g., "a+x")
            recursive (bool, optional): Whether to apply permissions recursively to directories
            
        Returns:
            Operation result
        """
        try:
            # Convert recursive to boolean if it's a string
            if isinstance(recursive, str):
                recursive = recursive.lower() in ('true', 'yes', 'y', '1')
            
            # Check if path exists
            if not os.path.exists(path):
                return {
                    "success": False,
                    "error": f"Path '{path}' does not exist"
                }
            
            # Convert mode to integer if given as octal string
            if isinstance(mode, str):
                if mode.isdigit():
                    # Convert from octal string (e.g., "755") to integer
                    mode = int(mode, 8)
                else:
                    # Handle symbolic mode (e.g., "u+x")
                    # This would require complex parsing or using a library like 'chmod'
                    return {
                        "success": False,
                        "error": f"Symbolic mode '{mode}' is not supported yet. Use numeric octal mode (e.g., 755)."
                    }
            
            # Prepare the result
            result = {
                "path": os.path.abspath(path),
                "type": "directory" if os.path.isdir(path) else "file",
                "mode": oct(mode)[2:],  # Convert integer to octal string without '0o' prefix
                "recursive": recursive,
                "success": True
            }
            
            # Apply permissions
            if recursive and os.path.isdir(path):
                # Count for reporting
                count = 0
                
                # Walk through the directory tree
                for root, dirs, files in os.walk(path):
                    # Change permissions for the current directory
                    os.chmod(root, mode)
                    count += 1
                    
                    # Change permissions for all files in the directory
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            os.chmod(file_path, mode)
                            count += 1
                        except Exception as e:
                            # Add warning but continue
                            if not "warnings" in result:
                                result["warnings"] = []
                            result["warnings"].append(f"Failed to change permissions for '{file_path}': {str(e)}")
                
                result["message"] = f"Changed permissions of '{path}' and its contents to {result['mode']} (recursive)"
                result["items_modified"] = count
            else:
                # Change permissions for a single file or directory
                os.chmod(path, mode)
                result["message"] = f"Changed permissions of '{path}' to {result['mode']}"
            
            return result
        except Exception as e:
            return {
                "success": False,
                "path": path,
                "error": str(e)
            }
            
    def _format_permissions(self, mode):
        """
        Formats numeric permission mode to human-readable format (e.g., 'rw-r--r--')
        
        Args:
            mode (int): The numeric permission mode
            
        Returns:
            str: Human-readable permission string
        """
        perm_string = ""
        
        # User permissions
        perm_string += 'r' if mode & stat.S_IRUSR else '-'
        perm_string += 'w' if mode & stat.S_IWUSR else '-'
        perm_string += 'x' if mode & stat.S_IXUSR else '-'
        
        # Group permissions
        perm_string += 'r' if mode & stat.S_IRGRP else '-'
        perm_string += 'w' if mode & stat.S_IWGRP else '-'
        perm_string += 'x' if mode & stat.S_IXGRP else '-'
        
        # Other permissions
        perm_string += 'r' if mode & stat.S_IROTH else '-'
        perm_string += 'w' if mode & stat.S_IWOTH else '-'
        perm_string += 'x' if mode & stat.S_IXOTH else '-'
        
        return perm_string

    def _get_symbolic_mode(self, mode):
        """
        Convierte un modo numérico a representación simbólica (como ls -l)
        
        Args:
            mode (int): Modo numérico (octal)
            
        Returns:
            str: Representación simbólica, e.g. 'rwxr-xr-x'
        """
        result = ""
        
        # Usuario
        result += 'r' if (mode & 0o400) else '-'
        result += 'w' if (mode & 0o200) else '-'
        result += 'x' if (mode & 0o100) else '-'
        
        # Grupo
        result += 'r' if (mode & 0o40) else '-'
        result += 'w' if (mode & 0o20) else '-'
        result += 'x' if (mode & 0o10) else '-'
        
        # Otros
        result += 'r' if (mode & 0o4) else '-'
        result += 'w' if (mode & 0o2) else '-'
        result += 'x' if (mode & 0o1) else '-'
        
        return result 