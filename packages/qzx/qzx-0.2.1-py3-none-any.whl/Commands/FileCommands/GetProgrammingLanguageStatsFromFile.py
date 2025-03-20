#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GetProgrammingLanguageStatsFromFile Command - Analyzes files to determine the programming language and statistics. Supports wildcards and recursive directory searches.
"""

import os
import re
import json
import glob
import fnmatch
from collections import Counter, defaultdict
import math
from pathlib import Path
from Core.command_base import CommandBase

class GetProgrammingLanguageStatsFromFileCommand(CommandBase):
    """
    Command to identify programming language in one or more files and get code statistics.
    Supports wildcards and recursive directory searching.
    """
    
    name = "getProgrammingLanguageStatsFromFile"
    description = "Analyzes files to determine the programming language and provides statistics about the code. Supports wildcards and recursive directory search."
    category = "file"
    
    parameters = [
        {
            'name': 'file_path',
            'description': 'Path to the file(s) to analyze. Supports wildcards like *.py',
            'required': True
        },
        {
            'name': 'detailed',
            'description': 'Whether to provide detailed statistics',
            'required': False,
            'default': False
        },
        {
            'name': 'languages',
            'description': 'Comma-separated list of languages to detect (default: all available)',
            'required': False,
            'default': None
        },
        {
            'name': 'recursive',
            'description': 'Recursion level: -r/--recursive for unlimited depth, -rN/--recursiveN for N levels deep',
            'required': False,
            'default': None
        }
    ]
    
    examples = [
        {
            'command': 'qzx getProgrammingLanguageStatsFromFile script.py',
            'description': 'Analyze a Python file to determine language statistics'
        },
        {
            'command': 'qzx getProgrammingLanguageStatsFromFile app.js true',
            'description': 'Analyze a JavaScript file with detailed statistics'
        },
        {
            'command': 'qzx getProgrammingLanguageStatsFromFile code.cpp false "cpp,c,python"',
            'description': 'Analyze a C++ file specifically checking for C++, C and Python patterns'
        },
        {
            'command': 'qzx getProgrammingLanguageStatsFromFile "*.js" false null -r',
            'description': 'Analyze all JavaScript files in current directory and all subdirectories'
        },
        {
            'command': 'qzx getProgrammingLanguageStatsFromFile "src/**/*.py" -r',
            'description': 'Analyze all Python files in src directory and subdirectories with detailed stats'
        },
        {
            'command': 'qzx getProgrammingLanguageStatsFromFile "*.py" true null -r2',
            'description': 'Analyze all Python files in current directory and up to 2 levels of subdirectories with detailed stats'
        }
    ]
    
    # Mapping of file extensions to language names
    LANGUAGE_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.php': 'PHP',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.cs': 'C#',
        '.go': 'Go',
        '.rb': 'Ruby',
        '.rs': 'Rust',
        '.ts': 'TypeScript',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.sh': 'Shell',
        '.bat': 'Batch',
        '.ps1': 'PowerShell',
        '.sql': 'SQL',
        '.r': 'R',
        '.pas': 'Pascal',
        '.pl': 'Perl',
        '.lua': 'Lua',
        '.vb': 'Visual Basic',
    }
    
    # Directory containing programming language dictionaries
    LANGUAGES_DIR = "Resources/ProgrammingLanguages"
    
    def _load_language_dictionaries(self, languages=None):
        """
        Load language dictionaries from JSON files
        
        Args:
            languages (list, optional): List of language names to load
            
        Returns:
            dict: Dictionary with language data
        """
        language_data = {}
        available_languages = []
        
        # Map some common case variations to standard names
        language_name_map = {
            'python': 'python',
            'javascript': 'javascript',
            'js': 'javascript',
            'java': 'java',
            'c++': 'cpp',
            'cpp': 'cpp',
            'c#': 'csharp',
            'csharp': 'csharp',
            'html': 'html',
            'css': 'css',
            'php': 'php',
            'ruby': 'ruby',
            'rust': 'rust',
            'typescript': 'typescript',
            'ts': 'typescript',
            'go': 'go',
            'golang': 'go',
            'sql': 'sql'
        }
        
        # Get list of available language files
        try:
            for file in os.listdir(self.LANGUAGES_DIR):
                if file.endswith('.json'):
                    lang_name = os.path.splitext(file)[0]
                    available_languages.append(lang_name)
        except FileNotFoundError:
            print(f"Warning: Languages directory '{self.LANGUAGES_DIR}' not found")
            return self._get_default_language_data()
            
        # If no languages specified, load all available
        if not languages:
            languages_to_load = available_languages
        else:
            # Normalize language names and map to available files
            languages_to_load = []
            for lang in languages:
                normalized = lang.lower()
                if normalized in language_name_map:
                    normalized = language_name_map[normalized]
                
                if normalized in available_languages:
                    languages_to_load.append(normalized)
                else:
                    print(f"Warning: Language '{lang}' not found in languages directory")
        
        # Load dictionaries for each language
        for lang in languages_to_load:
            try:
                dict_path = os.path.join(self.LANGUAGES_DIR, f"{lang}.json")
                if os.path.exists(dict_path):
                    with open(dict_path, 'r', encoding='utf-8') as f:
                        lang_data = json.load(f)
                    
                    # Standardize language name to title case
                    lang_name = lang.title()
                    language_data[lang_name] = lang_data
            except Exception as e:
                print(f"Error loading language data for '{lang}': {str(e)}")
        
        # If no languages were loaded, use defaults
        if not language_data:
            return self._get_default_language_data()
                
        return language_data
    
    def _get_default_language_data(self):
        """
        Fallback method to provide default language data
        
        Returns:
            dict: Dictionary with default language data
        """
        # Just include a few common languages
        return {
            'Python': {
                'keywords': [
                    'def', 'class', 'import', 'from', 'if', 'else', 'elif', 'for', 'while', 
                    'try', 'except', 'finally', 'with', 'as', 'lambda', 'return', 'yield'
                ],
                'comments': {
                    'single_line': [r'^\s*#'], 
                    'multi_line': [r'^\s*""".*?"""', r"^\s*'''.*?'''"]
                },
                'patterns': {
                    'function_definition': [r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('],
                    'class_definition': [r'^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]']
                }
            },
            'JavaScript': {
                'keywords': [
                    'function', 'var', 'let', 'const', 'if', 'else', 'for', 'while', 'switch', 
                    'case', 'break', 'return', 'try', 'catch', 'finally', 'class', 'extends',
                    'import', 'export', 'this', 'async', 'await'
                ],
                'comments': {
                    'single_line': [r'^\s*//'],
                    'multi_line': [r'/\*.*?\*/']
                },
                'patterns': {
                    'function_definition': [
                        r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(',
                        r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\(',
                        r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:\s*function\s*\('
                    ],
                    'class_definition': [r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)']
                }
            }
        }
        
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

    def _analyze_file(self, file_path, detailed=False, language_data=None):
        """
        Analyze a single file for programming language and code statistics
        
        Args:
            file_path (str): Path to the file to analyze
            detailed (bool): Whether to include detailed statistics
            language_data (dict): Pre-loaded language dictionaries
            
        Returns:
            dict: Analysis results for this file
        """
        try:
            # Check if the file exists and is a file
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                return {
                    "success": False,
                    "file_path": file_path,
                    "error": f"File does not exist or is not a regular file: {file_path}"
                }
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    lines = content.splitlines()
            except UnicodeDecodeError:
                # Try with different encoding if UTF-8 fails
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                        lines = content.splitlines()
                except Exception as e:
                    return {
                        "success": False,
                        "file_path": file_path,
                        "error": f"Failed to read file: {str(e)}"
                    }
            
            # Basic file stats
            file_size = os.path.getsize(file_path)
            line_count = len(lines)
            empty_lines = sum(1 for line in lines if not line.strip())
            
            # Detect language based on file extension
            _, file_extension = os.path.splitext(file_path)
            detected_language = self.LANGUAGE_EXTENSIONS.get(file_extension.lower(), 'Unknown')
            
            language_scores = {}
            
            # If language is still unknown or we want detailed analysis, analyze content
            if detected_language == 'Unknown' or detailed:
                language_scores = self._analyze_content(lines, content, language_data)
                
                # If language was unknown from extension, use the highest scoring one
                if detected_language == 'Unknown' and language_scores:
                    detected_language = max(language_scores.items(), key=lambda x: x[1])[0]
            
            # Get comment statistics if we know the language
            comment_stats = self._analyze_comments(lines, detected_language, language_data)
            
            # Get function/class count if we know the language
            functions = self._identify_functions(lines, detected_language, language_data)
            
            # Prepare the result
            result = {
                "success": True,
                "file_path": os.path.abspath(file_path),
                "file_name": os.path.basename(file_path),
                "file_extension": file_extension,
                "file_size": file_size,
                "file_size_readable": self._format_bytes(file_size),
                "detected_language": detected_language,
                "line_count": line_count,
                "empty_lines": empty_lines,
                "code_lines": line_count - empty_lines - comment_stats['comment_lines'],
                "comment_lines": comment_stats['comment_lines'],
                "comment_percentage": round((comment_stats['comment_lines'] / line_count * 100) if line_count > 0 else 0, 2),
                "functions_count": len(functions),
                "functions": functions if detailed else [],
            }
            
            # Add detailed language scores if available
            if language_scores and detailed:
                # Normalize scores for easier comparison
                total_score = sum(language_scores.values())
                normalized_scores = {}
                
                if total_score > 0:
                    for lang, score in language_scores.items():
                        normalized_scores[lang] = round((score / total_score) * 100, 2)
                
                result["language_confidence"] = normalized_scores
            
            # Add keyword stats if detailed
            if detailed:
                result["keyword_stats"] = self._analyze_keywords(content, detected_language, language_data)
                
                # Add complexity metrics
                result["complexity"] = self._estimate_complexity(lines, detected_language, functions)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e)
            }
    
    def execute(self, file_path, detailed=False, languages=None, recursive=None):
        """
        Analyzes one or more files to determine programming language and code statistics.
        Supports wildcards and recursive directory search.
        
        Args:
            file_path (str): Path to the file(s) to analyze. Supports wildcards like *.py
            detailed (bool, optional): Whether to include detailed statistics
            languages (str, optional): Comma-separated list of languages to detect
            recursive: Recursion level: none by default, -r/--recursive for unlimited, -rN/--recursiveN for N levels
            
        Returns:
            Dictionary with analysis results for each file and aggregated statistics
        """
        try:
            # Convert boolean parameters if they're strings
            if isinstance(detailed, str):
                detailed = detailed.lower() in ('true', 'yes', 'y', '1')
            
            # Parse recursion parameter
            recursion_depth = self._parse_recursive_parameter(recursive)
            
            # Parse the languages parameter if provided
            lang_list = None
            if languages:
                if isinstance(languages, str):
                    if languages.lower() == 'null' or languages.lower() == 'none':
                        lang_list = None
                    else:
                        lang_list = [lang.strip() for lang in languages.split(',')]
                elif isinstance(languages, list):
                    lang_list = languages
            
            # Load language dictionaries
            language_data = self._load_language_dictionaries(lang_list)
            
            # Find files matching the pattern
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
            
            # Analyze each file
            file_results = []
            extensions_found = set()
            languages_found = set()
            total_size = 0
            total_lines = 0
            total_blank_lines = 0
            total_comment_lines = 0
            total_code_lines = 0
            total_files = 0
            
            for single_file_path in matching_files:
                result = self._analyze_file(single_file_path, detailed, language_data)
                file_results.append(result)
                
                # Count successful analyses
                if result.get('success', False):
                    total_files += 1
                    total_size += result.get('file_size', 0)
                    total_lines += result.get('line_count', 0)
                    total_blank_lines += result.get('empty_lines', 0)
                    total_comment_lines += result.get('comment_lines', 0)
                    total_code_lines += result.get('code_lines', 0)
                    extensions_found.add(result.get('file_extension', 'Unknown'))
                    languages_found.add(result.get('detected_language', 'Unknown'))
            
            # Get a descriptive recursion string for the result
            recursion_info = "unlimited"
            if recursion_depth == 0:
                recursion_info = "none"
            elif recursion_depth is not None:
                recursion_info = str(recursion_depth)
            
            # Calculate percentages
            if total_lines > 0:
                blank_percent = (total_blank_lines / total_lines) * 100
                comment_percent = (total_comment_lines / total_lines) * 100
                code_percent = (total_code_lines / total_lines) * 100
            else:
                blank_percent = 0
                comment_percent = 0
                code_percent = 0
            
            # Sort languages by lines of code
            language_stats_sorted = sorted(language_stats.items(), key=lambda x: x[1].get('code_lines', 0), reverse=True)
            
            # Prepare the final result
            result = {
                "success": True,
                "file_pattern": file_path,
                "recursive": recursion_info,
                "detailed": detailed,
                "files_analyzed": total_files,
                "total_size": total_size,
                "total_size_readable": self._format_bytes(total_size),
                "total_lines": total_lines,
                "total_blank_lines": total_blank_lines,
                "total_comment_lines": total_comment_lines,
                "total_code_lines": total_code_lines,
                "blank_percent": round(blank_percent, 1),
                "comment_percent": round(comment_percent, 1),
                "code_percent": round(code_percent, 1),
                "languages_found": list(languages_found),
                "extensions_found": list(extensions_found),
                "language_stats": [
                    {
                        "language": lang,
                        "files": stats.get('files', 0),
                        "lines": stats.get('total_lines', 0),
                        "blank_lines": stats.get('blank_lines', 0),
                        "comment_lines": stats.get('comment_lines', 0),
                        "code_lines": stats.get('code_lines', 0),
                        "extensions": stats.get('extensions', [])
                    }
                    for lang, stats in language_stats_sorted
                ],
                "files": file_results
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "file_pattern": file_path,
                "error": str(e)
            }
    
    def _analyze_content(self, lines, content, language_data):
        """
        Analyze file content to determine language based on keywords
        
        Args:
            lines (list): List of file lines
            content (str): Full file content
            language_data (dict): Dictionary with language data
            
        Returns:
            dict: Dictionary with language scores
        """
        language_scores = {}
        
        # Check for language-specific keywords
        for language, lang_dict in language_data.items():
            # Calculate a score based on keyword matches
            score = 0
            
            # Check all types of language elements, not just keywords
            for element_type in ['keywords', 'builtins', 'global_functions', 'dom_objects']:
                if element_type in lang_dict:
                    keywords = lang_dict[element_type]
                    for keyword in keywords:
                        # Create a regex pattern that matches the keyword as a whole word
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        score += len(matches)
            
            # Check patterns
            if 'patterns' in lang_dict:
                for pattern_type, patterns in lang_dict['patterns'].items():
                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        score += len(matches) * 2  # Give more weight to patterns
            
            if score > 0:
                language_scores[language] = score
            
        return language_scores
    
    def _analyze_comments(self, lines, language, language_data):
        """
        Analyze code comments in the file
        
        Args:
            lines (list): List of file lines
            language (str): Detected programming language
            language_data (dict): Dictionary with language data
            
        Returns:
            dict: Dictionary with comment statistics
        """
        comment_lines = 0
        
        # Get language data
        lang_dict = language_data.get(language, {})
        
        # Get comment patterns for the language
        patterns = lang_dict.get('comments', {'single_line': [], 'multi_line': []})
        
        # If no patterns found in the language data, use the old way
        if not patterns.get('single_line') and not patterns.get('multi_line'):
            # Fall back to original method
            return self._analyze_comments_legacy(lines, language)
        
        # Join all lines for multi-line comment detection
        full_content = "\n".join(lines)
        
        # First check for multi-line comments with regex
        for pattern in patterns.get('multi_line', []):
            # Find all multi-line comments
            for match in re.finditer(pattern, full_content, re.DOTALL):
                # Count newlines in the match
                comment_lines += match.group(0).count('\n') + 1
        
        # Then check for single-line comments
        for i, line in enumerate(lines):
            line_is_comment = False
            
            # Check if line matches any single-line comment pattern
            for pattern in patterns.get('single_line', []):
                if re.search(pattern, line):
                    line_is_comment = True
                    break
            
            if line_is_comment:
                comment_lines += 1
        
        return {
            "comment_lines": comment_lines
        }
    
    def _analyze_comments_legacy(self, lines, language):
        """
        Legacy method for analyzing comments
        
        Args:
            lines (list): List of file lines
            language (str): Detected programming language
            
        Returns:
            dict: Dictionary with comment statistics
        """
        comment_lines = 0
        in_multiline_comment = False
        multiline_comment_text = ""
        
        # Old comment patterns dictionary
        comment_patterns = {
            'Python': {
                'single_line': [r'^\s*#'],
                'multi_line': [r'^\s*""".*?"""', r"^\s*'''.*?'''"]
            },
            'JavaScript': {
                'single_line': [r'^\s*//'],
                'multi_line': [r'/\*.*?\*/']
            },
            'Java': {
                'single_line': [r'^\s*//'],
                'multi_line': [r'/\*.*?\*/']
            },
            'C++': {
                'single_line': [r'^\s*//'],
                'multi_line': [r'/\*.*?\*/']
            },
            'PHP': {
                'single_line': [r'^\s*(//|#)'],
                'multi_line': [r'/\*.*?\*/']
            },
            'Pascal': {
                'single_line': [r'^\s*//'],
                'multi_line': [r'\{.*?\}', r'\(\*.*?\*\)']
            },
            'HTML': {
                'single_line': [],
                'multi_line': [r'<!--.*?-->']
            },
            'CSS': {
                'single_line': [],
                'multi_line': [r'/\*.*?\*/']
            },
            'SQL': {
                'single_line': [r'^\s*--'],
                'multi_line': [r'/\*.*?\*/']
            }
        }
        
        # Get comment patterns for the language
        patterns = comment_patterns.get(language, {'single_line': [], 'multi_line': []})
        
        # Join all lines for multi-line comment detection
        full_content = "\n".join(lines)
        
        # First check for multi-line comments with regex
        for pattern in patterns.get('multi_line', []):
            # Find all multi-line comments
            for match in re.finditer(pattern, full_content, re.DOTALL):
                # Count newlines in the match
                comment_lines += match.group(0).count('\n') + 1
        
        # Then check for single-line comments
        for i, line in enumerate(lines):
            line_is_comment = False
            
            # Check if line matches any single-line comment pattern
            for pattern in patterns.get('single_line', []):
                if re.search(pattern, line):
                    line_is_comment = True
                    break
            
            if line_is_comment:
                comment_lines += 1
        
        return {
            "comment_lines": comment_lines
        }
    
    def _identify_functions(self, lines, language, language_data):
        """
        Identify function declarations in the file
        
        Args:
            lines (list): List of file lines
            language (str): Detected programming language
            language_data (dict): Dictionary with language data
            
        Returns:
            list: List of identified function names
        """
        functions = []
        
        # Get language data
        lang_dict = language_data.get(language, {})
        
        # Get patterns for the language
        pattern_dict = lang_dict.get('patterns', {})
        
        # Combine function and class definition patterns
        patterns = pattern_dict.get('function_definition', []) + pattern_dict.get('class_definition', [])
        
        # If no patterns found in the language data, use the legacy approach
        if not patterns:
            return self._identify_functions_legacy(lines, language)
        
        # Check each line for function declarations
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    # Get the function name from the regex group
                    if len(match.groups()) >= 1:
                        # The function name might be in different group indexes depending on the pattern
                        # Try to get the last group which is usually the name
                        func_name = match.groups()[-1]
                        
                        # Determine if it's a class or function based on pattern
                        func_type = "class" if "class" in pattern.lower() else "function"
                        
                        functions.append({
                            "name": func_name,
                            "line": i + 1,
                            "type": func_type
                        })
        
        return functions
    
    def _identify_functions_legacy(self, lines, language):
        """
        Legacy method for identifying functions
        
        Args:
            lines (list): List of file lines
            language (str): Detected programming language
            
        Returns:
            list: List of identified function names
        """
        functions = []
        
        # Legacy function patterns
        function_patterns = {
            'Python': [
                r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
                r'^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]'
            ],
            'JavaScript': [
                r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(',
                r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\(',
                r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:\s*function\s*\(',
                r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)',
                r'(async\s+)?([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(\s*[^)]*\)\s*{',
                r'(get|set|async)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
            ],
            'Java': [
                r'(public|private|protected|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\)',
                r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)'
            ],
            'C++': [
                r'([\w\*]+\s+)+(\w+)\s*\([^)]*\)\s*(\{|:)',
                r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            ],
            'PHP': [
                r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
                r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            ],
            'Pascal': [
                r'procedure\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                r'program\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                r'unit\s+([a-zA-Z_][a-zA-Z0-9_]*)'
            ]
        }
        
        # Get patterns for the language
        patterns = function_patterns.get(language, [])
        
        # Check each line for function declarations
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    # Get the function name from the regex group
                    if len(match.groups()) >= 1:
                        # Try to get the most likely function name
                        # Usually the last group is the actual name
                        func_name = match.groups()[-1]
                        
                        functions.append({
                            "name": func_name,
                            "line": i + 1,
                            "type": "class" if 'class' in pattern else "function"
                        })
        
        return functions
    
    def _analyze_keywords(self, content, language, language_data):
        """
        Analyze keyword usage in the file
        
        Args:
            content (str): File content
            language (str): Detected programming language
            language_data (dict): Dictionary with language data
            
        Returns:
            dict: Dictionary with keyword statistics
        """
        keyword_stats = {}
        
        # Get language data
        lang_dict = language_data.get(language, {})
        
        # Combine all word lists that are worth counting
        all_keywords = []
        for key in ['keywords', 'builtins', 'global_functions']:
            if key in lang_dict:
                all_keywords.extend(lang_dict[key])
        
        # If no keywords found, return empty stats
        if not all_keywords:
            return keyword_stats
        
        # Count occurrences of each keyword
        for keyword in all_keywords:
            # Create a regex pattern that matches the keyword as a whole word
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, content, re.IGNORECASE)
            count = len(matches)
            
            if count > 0:
                keyword_stats[keyword] = count
        
        # Sort by frequency
        return dict(sorted(keyword_stats.items(), key=lambda item: item[1], reverse=True))
    
    def _estimate_complexity(self, lines, language, functions):
        """
        Estimate code complexity metrics
        
        Args:
            lines (list): List of file lines
            language (str): Detected programming language
            functions (list): Identified functions
            
        Returns:
            dict: Dictionary with complexity metrics
        """
        # Basic cyclomatic complexity estimation
        complexity_keywords = [
            r'\bif\b', r'\belse\b', r'\bfor\b', r'\bwhile\b', r'\bcase\b',
            r'\bcatch\b', r'\b\|\|\b', r'\b&&\b', r'\?', r':\s*\w+'
        ]
        
        # Count branching statements
        branching_count = 0
        for line in lines:
            for keyword in complexity_keywords:
                matches = re.findall(keyword, line)
                branching_count += len(matches)
        
        # Calculate average function length
        avg_function_length = 0
        if functions:
            # Sort functions by line number
            sorted_funcs = sorted(functions, key=lambda x: x['line'])
            
            # Estimate function lengths
            lengths = []
            for i in range(len(sorted_funcs)):
                if i < len(sorted_funcs) - 1:
                    length = sorted_funcs[i+1]['line'] - sorted_funcs[i]['line']
                else:
                    # For the last function, assume it extends to the end
                    length = len(lines) - sorted_funcs[i]['line'] + 1
                
                # Apply a reasonable cap to avoid outliers
                length = min(length, 200)
                lengths.append(length)
            
            avg_function_length = sum(lengths) / len(lengths) if lengths else 0
        
        # Calculate a rough maintainability index
        # Based on a simplified version of the Microsoft metric
        # MI = 171 - 5.2 * ln(aveV) - 0.23 * aveV(g') - 16.2 * ln(aveLOC)
        loc = len(lines)
        avg_loc_per_function = avg_function_length if avg_function_length > 0 else loc
        
        halstead_volume = math.log(len(set(("".join(lines)).split()))) * len(lines) if lines else 0
        cyclomatic_complexity = 1 + branching_count
        
        maintainability = 171
        maintainability -= 5.2 * math.log(halstead_volume + 1)
        maintainability -= 0.23 * cyclomatic_complexity
        maintainability -= 16.2 * math.log(avg_loc_per_function + 1)
        
        # Normalize to 0-100 scale
        maintainability = max(0, min(100, maintainability))
        
        return {
            "cyclomatic_complexity": cyclomatic_complexity,
            "branching_statements": branching_count,
            "avg_function_length": round(avg_function_length, 2),
            "maintainability_index": round(maintainability, 2),
            "complexity_rating": self._get_complexity_rating(maintainability)
        }
    
    def _get_complexity_rating(self, maintainability):
        """
        Convert maintainability index to a human-readable rating
        
        Args:
            maintainability (float): Maintainability index
            
        Returns:
            str: Complexity rating
        """
        if maintainability >= 85:
            return "Highly Maintainable"
        elif maintainability >= 65:
            return "Maintainable"
        elif maintainability >= 40:
            return "Moderately Maintainable"
        else:
            return "Difficult to Maintain"
    
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