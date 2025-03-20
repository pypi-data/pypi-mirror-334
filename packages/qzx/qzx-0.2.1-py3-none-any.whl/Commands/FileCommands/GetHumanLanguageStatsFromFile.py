#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GetHumanLanguageStatsFromFile Command - Analyzes text files to determine the percentage of content in different languages
"""

import os
import re
import json
import glob
from collections import defaultdict
from pathlib import Path
from Core.command_base import CommandBase

class GetHumanLanguageStatsFromFileCommand(CommandBase):
    """
    Command to analyze a file or multiple files and determine the percentage of text in different languages,
    intelligently filtering out programming code. Supports wildcards and recursive directory search.
    """
    
    name = "getHumanLanguageStatsFromFile"
    description = "Analyzes files to determine the percentage of text in different languages. Supports wildcards and recursive directory search."
    category = "file"
    
    parameters = [
        {
            'name': 'file_path',
            'description': 'Path to the file(s) to analyze. Supports wildcards like *.txt',
            'required': True
        },
        {
            'name': 'ignore_comments',
            'description': 'Whether to ignore code comments when analyzing text',
            'required': False,
            'default': False
        },
        {
            'name': 'min_word_length',
            'description': 'Minimum length of words to consider for language detection',
            'required': False,
            'default': 4
        },
        {
            'name': 'languages',
            'description': 'Comma-separated list of languages to detect (default: all available)',
            'required': False,
            'default': None
        },
        {
            'name': 'recursive',
            'description': 'Whether to search recursively in directories',
            'required': False,
            'default': False
        }
    ]
    
    examples = [
        {
            'command': 'qzx getHumanLanguageStatsFromFile myfile.txt',
            'description': 'Analyze language distribution in a text file'
        },
        {
            'command': 'qzx getHumanLanguageStatsFromFile code.py true',
            'description': 'Analyze a Python file, ignoring code comments'
        },
        {
            'command': 'qzx getHumanLanguageStatsFromFile "*.md" false 3',
            'description': 'Analyze all Markdown files in current directory'
        },
        {
            'command': 'qzx getHumanLanguageStatsFromFile "docs/*.txt" false 3 "english,spanish,french"',
            'description': 'Analyze text files in docs directory for specific languages only'
        },
        {
            'command': 'qzx getHumanLanguageStatsFromFile "src/**/*.py" true 4 null true',
            'description': 'Analyze all Python files recursively in src directory'
        }
    ]
    
    # Common programming language patterns to filter out
    CODE_PATTERNS = {
        'python': [
            r'def\s+\w+\s*\(.*?\):',  # Function definitions
            r'class\s+\w+(\s*\(.*?\))?:',  # Class definitions
            r'import\s+[\w\.]+',  # Import statements
            r'from\s+[\w\.]+\s+import',  # From import statements
            r'if\s+.*?:',  # If statements
            r'elif\s+.*?:',  # Elif statements
            r'else:',  # Else statements
            r'while\s+.*?:',  # While loops
            r'for\s+.*?\s+in\s+.*?:',  # For loops
            r'try:',  # Try blocks
            r'except(\s+.*?)?:',  # Except blocks
            r'finally:',  # Finally blocks
            r'with\s+.*?:',  # With statements
            r'@\w+',  # Decorators
            r'return\s+.*',  # Return statements
            r'yield\s+.*',  # Yield statements
            r'self\.',  # Self references
            r'super\(',  # Super calls
            r'lambda\s+.*?:',  # Lambda expressions
            r'raise\s+.*',  # Raise statements
            r'assert\s+.*',  # Assert statements
            r'print\(',  # Print functions
        ],
        'javascript': [
            r'function\s+\w+\s*\(.*?\)',  # Function definitions
            r'const\s+\w+\s*=',  # Const declarations
            r'let\s+\w+\s*=',  # Let declarations
            r'var\s+\w+\s*=',  # Var declarations
            r'class\s+\w+\s*{',  # Class definitions
            r'import\s+.*?from',  # Import statements
            r'export\s+',  # Export statements
            r'if\s*\(.*?\)',  # If statements
            r'else\s+if\s*\(.*?\)',  # Else if statements
            r'else\s*{',  # Else statements
            r'for\s*\(.*?\)',  # For loops
            r'while\s*\(.*?\)',  # While loops
            r'switch\s*\(.*?\)',  # Switch statements
            r'case\s+.*?:',  # Case statements
            r'try\s*{',  # Try blocks
            r'catch\s*\(.*?\)',  # Catch blocks
            r'finally\s*{',  # Finally blocks
            r'new\s+\w+',  # New operator
            r'return\s+.*',  # Return statements
            r'this\.',  # This references
            r'=>\s*{',  # Arrow functions
            r'console\.',  # Console statements
            r'document\.',  # Document references
            r'window\.',  # Window references
        ],
        'c': [
            r'#include\s+[<"].*?[>"]',  # Include statements
            r'#define\s+\w+',  # Define statements
            r'#ifdef\s+\w+',  # Ifdef statements
            r'#ifndef\s+\w+',  # Ifndef statements
            r'#endif',  # Endif statements
            r'int\s+\w+\s*\(.*?\)',  # Int function definitions
            r'void\s+\w+\s*\(.*?\)',  # Void function definitions
            r'char\s+\w+\s*\(.*?\)',  # Char function definitions
            r'float\s+\w+\s*\(.*?\)',  # Float function definitions
            r'double\s+\w+\s*\(.*?\)',  # Double function definitions
            r'struct\s+\w+\s*{',  # Struct definitions
            r'typedef\s+',  # Typedef statements
            r'enum\s+\w+\s*{',  # Enum definitions
            r'union\s+\w+\s*{',  # Union definitions
            r'if\s*\(.*?\)',  # If statements
            r'else\s+if\s*\(.*?\)',  # Else if statements
            r'else\s*{',  # Else statements
            r'for\s*\(.*?\)',  # For loops
            r'while\s*\(.*?\)',  # While loops
            r'do\s*{',  # Do-while loops
            r'switch\s*\(.*?\)',  # Switch statements
            r'case\s+.*?:',  # Case statements
            r'break;',  # Break statements
            r'continue;',  # Continue statements
            r'return\s+.*?;',  # Return statements
            r'goto\s+\w+;',  # Goto statements
            r'printf\(',  # Printf function calls
            r'scanf\(',  # Scanf function calls
            r'malloc\(',  # Malloc function calls
            r'free\(',  # Free function calls
        ],
        'rust': [
            r'fn\s+\w+\s*\(.*?\)',  # Function definitions
            r'struct\s+\w+\s*{',  # Struct definitions
            r'enum\s+\w+\s*{',  # Enum definitions
            r'trait\s+\w+\s*{',  # Trait definitions
            r'impl\s+.*?\s*{',  # Impl blocks
            r'let\s+\w+\s*=',  # Let declarations
            r'let\s+mut\s+\w+',  # Mutable let declarations
            r'const\s+\w+:',  # Const declarations
            r'static\s+\w+:',  # Static declarations
            r'use\s+.*?;',  # Use statements
            r'mod\s+\w+;',  # Mod declarations
            r'pub\s+',  # Pub declarations
            r'if\s+.*?\s*{',  # If statements
            r'else\s+if\s+.*?\s*{',  # Else if statements
            r'else\s*{',  # Else statements
            r'match\s+.*?\s*{',  # Match statements
            r'for\s+.*?\s+in\s+.*?\s*{',  # For loops
            r'while\s+.*?\s*{',  # While loops
            r'loop\s*{',  # Loop statements
            r'break;',  # Break statements
            r'continue;',  # Continue statements
            r'return\s+.*?;',  # Return statements
            r'self\.',  # Self references
            r'println!\(',  # Println macro
            r'format!\(',  # Format macro
            r'vec!\[',  # Vec macro
            r'->\s*\w+',  # Return type annotations
            r'&mut\s+',  # Mutable references
            r'&\w+',  # References
        ],
        'common': [
            r'[a-z0-9_]+\.[a-z0-9_]+\(',  # Method calls
            r'\(\s*[a-z0-9_]+\s*\)',  # Function calls with single argument
            r'\(\s*[a-zA-Z0-9_]+\s*,\s*[a-zA-Z0-9_]+\s*\)',  # Function calls with two arguments
            r'{.*?}',  # Curly brace blocks
            r'\[.*?\]',  # Square bracket blocks
            r'\(.*?\)',  # Parenthesis blocks
            r'[a-zA-Z0-9_]+\s*=\s*[a-zA-Z0-9_]+',  # Assignments
            r'[a-zA-Z0-9_]+\s*\+=\s*[a-zA-Z0-9_]+',  # Addition assignments
            r'[a-zA-Z0-9_]+\s*-=\s*[a-zA-Z0-9_]+',  # Subtraction assignments
            r'[a-zA-Z0-9_]+\s*\*=\s*[a-zA-Z0-9_]+',  # Multiplication assignments
            r'[a-zA-Z0-9_]+\s*/=\s*[a-zA-Z0-9_]+',  # Division assignments
            r'[a-zA-Z0-9_]+\+\+',  # Increment
            r'[a-zA-Z0-9_]+--',  # Decrement
            r'==|!=|<=|>=|&&|\|\|',  # Common operators
        ]
    }
    
    # Common comment patterns to identify comments
    COMMENT_PATTERNS = {
        'python': [
            r'#.*?$',  # Single line comments
            r'""".*?"""',  # Triple double quote docstrings
            r"'''.*?'''",  # Triple single quote docstrings
        ],
        'javascript': [
            r'//.*?$',  # Single line comments
            r'/\*.*?\*/',  # Multi-line comments
        ],
        'c': [
            r'//.*?$',  # Single line comments
            r'/\*.*?\*/',  # Multi-line comments
        ],
        'rust': [
            r'//.*?$',  # Single line comments
            r'/\*.*?\*/',  # Multi-line comments
        ],
        'html': [
            r'<!--.*?-->',  # HTML comments
        ]
    }
    
    # Mappings for language specific word endings
    LANGUAGE_WORD_ENDINGS = {
        'english': ['ing', 'ly', 'ed', 'th', 'ght', 'tion', 'sion', 'ment', 'ness', 'ful', 'ism', 'ist', 'ity', 'ous'],
        'spanish': ['ando', 'endo', 'ción', 'dad', 'mente', 'idad', 'oso', 'osa', 'miento', 'ito', 'ita', 'ador', 'adora'],
        'french': ['ment', 'ement', 'eux', 'euse', 'ère', 'elle', 'tion', 'isme', 'iste', 'ité', 'ant', 'ance', 'ence', 'oir'],
        'italian': ['mente', 'zione', 'mento', 'tore', 'trice', 'ista', 'ità', 'ismo', 'etto', 'etta', 'issimo', 'issima'],
        'portuguese': ['mente', 'ção', 'dade', 'idade', 'ante', 'ista', 'ismo', 'izar', 'mento', 'oso', 'osa', 'vel', 'eza'],
        'german': ['ung', 'heit', 'keit', 'schaft', 'isch', 'lich', 'bar', 'sam', 'los', 'haft', 'reich', 'voll']
    }
    
    # Path to function words dictionaries
    FUNCTION_WORDS_DIR = "Resources/FunctionWords"

    def _load_function_words(self, languages=None):
        """
        Load function words dictionaries for specified languages or all available
        
        Args:
            languages (list, optional): List of language names to load
            
        Returns:
            dict: Dictionary with language names as keys and function words as values
        """
        function_words = {}
        available_languages = []
        
        # Check if FunctionWords directory exists
        if not os.path.exists(self.FUNCTION_WORDS_DIR):
            print(f"Warning: FunctionWords directory not found at {self.FUNCTION_WORDS_DIR}")
            return self._get_default_function_words()
            
        # Get available language files
        for filename in os.listdir(self.FUNCTION_WORDS_DIR):
            if filename.endswith('.json'):
                lang = os.path.splitext(filename)[0].lower()
                available_languages.append(lang)
                
        # If no specific languages requested, load all available
        if not languages:
            languages_to_load = available_languages
        else:
            languages_to_load = []
            for lang in languages:
                lang = lang.lower()
                if lang in available_languages:
                    languages_to_load.append(lang)
                else:
                    print(f"Warning: Language '{lang}' not found in function words directory")
        
        # Load each language dictionary
        for lang in languages_to_load:
            try:
                file_path = os.path.join(self.FUNCTION_WORDS_DIR, f"{lang}.json")
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Extract words from the JSON structure
                    word_set = set()
                    
                    def extract_words(obj):
                        if isinstance(obj, dict):
                            for key, value in obj.items():
                                extract_words(value)
                        elif isinstance(obj, list):
                            for item in obj:
                                if isinstance(item, str):
                                    word_set.add(item.lower())
                                else:
                                    extract_words(item)
                    
                    extract_words(data)
                    function_words[lang] = word_set
            except Exception as e:
                print(f"Error loading function words for language '{lang}': {str(e)}")
                
        return function_words
        
    def _get_default_function_words(self):
        """
        Returns default function words if no dictionaries are found
        
        Returns:
            dict: Dictionary with default function words
        """
        return {
            'english': set([
                'the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but',
                'his', 'from', 'they', 'say', 'her', 'she', 'will', 'one', 'all', 'would',
                'there', 'their', 'what', 'out', 'about', 'who', 'get', 'which', 'when', 'make',
                'can', 'like', 'time', 'just', 'him', 'know', 'take', 'people', 'into', 'year',
                'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now',
                'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use',
                'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want'
            ]),
            'spanish': set([
                'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 
                'no', 'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le',
                'lo', 'todo', 'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir',
                'otro', 'ese', 'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él',
                'muy', 'sin', 'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo',
                'yo', 'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero', 'desde'
            ])
        }

    def _find_files(self, file_path_pattern, recursive=False):
        """
        Find files matching the given pattern, with optional recursive search
        
        Args:
            file_path_pattern (str): File path pattern (may include wildcards)
            recursive (bool): Whether to search recursively in directories
            
        Returns:
            list: List of file paths matching the pattern
        """
        # Handle Windows paths
        file_path_pattern = file_path_pattern.replace('\\', '/')
        
        if not any(char in file_path_pattern for char in '*?[]'):
            # No wildcard - direct file or directory
            if os.path.isfile(file_path_pattern):
                return [file_path_pattern]
            elif os.path.isdir(file_path_pattern):
                # If it's a directory and recursive is True, get all files recursively
                if recursive:
                    result = []
                    for root, _, files in os.walk(file_path_pattern):
                        for file in files:
                            result.append(os.path.join(root, file))
                    return result
                else:
                    # Just get files in the top directory
                    return [os.path.join(file_path_pattern, f) for f in os.listdir(file_path_pattern) 
                            if os.path.isfile(os.path.join(file_path_pattern, f))]
            else:
                return []
        
        # Handle glob patterns with recursive option
        if '**' in file_path_pattern and recursive:
            # Recursive glob pattern
            return glob.glob(file_path_pattern, recursive=True)
        elif recursive:
            # If recursive is True but '**' is not in pattern, modify the pattern
            # First check if there's a directory part in the pattern
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
            # Non-recursive glob
            return glob.glob(file_path_pattern)

    def _analyze_file(self, file_path, ignore_comments=False, min_word_length=4, function_words=None):
        """
        Analyze a single file for language content
        
        Args:
            file_path (str): Path to the file to analyze
            ignore_comments (bool): Whether to ignore code comments
            min_word_length (int): Minimum word length to consider
            function_words (dict): Dictionary of function words by language
            
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
            
            # Determine the file type from the extension
            _, ext = os.path.splitext(file_path)
            file_type = ext.lower().strip('.')
            
            # Map file extensions to language type
            language_map = {
                'py': 'python',
                'js': 'javascript',
                'jsx': 'javascript',
                'ts': 'javascript',
                'tsx': 'javascript',
                'c': 'c',
                'h': 'c',
                'cpp': 'c',
                'hpp': 'c',
                'rs': 'rust',
                'html': 'html',
                'htm': 'html',
                'css': 'css',
                'md': 'markdown',
                'txt': 'text',
                'json': 'json',
                'yaml': 'yaml',
                'yml': 'yaml',
                'xml': 'xml',
            }
            
            file_language = language_map.get(file_type, 'text')
            
            # Read the file
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
            except Exception as e:
                return {
                    "success": False,
                    "file_path": file_path,
                    "error": f"Error reading file: {str(e)}"
                }
            
            # Extract comments if they should be included in analysis
            comments_text = ""
            if not ignore_comments and file_language in self.COMMENT_PATTERNS:
                for pattern in self.COMMENT_PATTERNS[file_language]:
                    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
                    for match in matches:
                        comments_text += match + "\n"
            
            # Filter out code patterns from the content
            filtered_content = content
            
            # Apply language-specific code patterns
            if file_language in self.CODE_PATTERNS:
                for pattern in self.CODE_PATTERNS[file_language]:
                    filtered_content = re.sub(pattern, "", filtered_content, flags=re.MULTILINE | re.DOTALL)
            
            # Apply common code patterns
            for pattern in self.CODE_PATTERNS['common']:
                filtered_content = re.sub(pattern, "", filtered_content, flags=re.MULTILINE | re.DOTALL)
            
            # Remove remaining code-like elements
            filtered_content = re.sub(r'[\{\}\[\]\(\)=<>+\-*/&|!~%^]', ' ', filtered_content)
            
            # Replace multiple spaces with a single space
            filtered_content = re.sub(r'\s+', ' ', filtered_content).strip()
            
            # Add comments back if requested
            if not ignore_comments and comments_text:
                filtered_content += " " + comments_text
            
            # Split the filtered content into words - extended to handle non-Latin characters
            # This regex includes Latin, Greek, Cyrillic, Han (Chinese), Hiragana, Katakana, and Arabic script
            words = re.findall(r'\b[\w\u0370-\u03FF\u0400-\u04FF\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0600-\u06FF]+\b', filtered_content.lower())
            
            # Initialize language counts
            language_counts = {lang: 0 for lang in function_words.keys()}
            undetermined_count = 0
            
            # Count words by language
            for word in words:
                if len(word) >= min_word_length:
                    word_matched = False
                    
                    # Check each language's function words
                    for lang, word_set in function_words.items():
                        if word in word_set:
                            language_counts[lang] += 1
                            word_matched = True
                            break
                    
                    # If word not matched, try language-specific word endings
                    if not word_matched:
                        ending_matched = False
                        for lang, endings in self.LANGUAGE_WORD_ENDINGS.items():
                            if lang in function_words:  # Only check enabled languages
                                for ending in endings:
                                    if word.endswith(ending):
                                        language_counts[lang] += 1
                                        ending_matched = True
                                        break
                                if ending_matched:
                                    break
                        
                        # If still not matched, count as undetermined
                        if not ending_matched:
                            undetermined_count += 1
            
            total_determined = sum(language_counts.values())
            total_words = total_determined + undetermined_count
            
            # Prepare the result
            result = {
                "success": True,
                "file_path": os.path.abspath(file_path),
                "file_type": file_type,
                "detected_language_type": file_language,
                "total_words": len(words),
                "analyzed_words": total_words,
                "undetermined_words": undetermined_count,
                "language_stats": {}
            }
            
            # Add word counts for each language
            for lang, count in language_counts.items():
                result[f"{lang}_words"] = count
            
            # Calculate percentages for determined words
            if total_determined > 0:
                for lang, count in language_counts.items():
                    lang_percent = (count / total_determined) * 100
                    result["language_stats"][f"{lang}_percent"] = round(lang_percent, 2)
                
                # Determine primary language
                primary_lang = max(language_counts.items(), key=lambda x: x[1])
                if primary_lang[1] > 0:
                    result["primary_language"] = primary_lang[0].capitalize()
                else:
                    result["primary_language"] = "Undetermined"
            else:
                for lang in language_counts.keys():
                    result["language_stats"][f"{lang}_percent"] = 0
                result["primary_language"] = "Undetermined"
            
            # Add undetermined percentage
            if total_words > 0:
                undetermined_percent = (undetermined_count / total_words) * 100
                result["language_stats"]["undetermined_percent"] = round(undetermined_percent, 2)
            else:
                result["language_stats"]["undetermined_percent"] = 100
                
            return result
            
        except Exception as e:
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e)
            }

    def execute(self, file_path, ignore_comments=False, min_word_length=4, languages=None, recursive=False):
        """
        Analyzes one or more files to determine the percentage of text in different languages.
        Supports wildcards and recursive directory search.
        
        Args:
            file_path (str): Path to the file(s) to analyze. Supports wildcards like *.txt
            ignore_comments (bool, optional): Whether to ignore code comments when analyzing text
            min_word_length (int, optional): Minimum length of words to consider for language detection
            languages (str, optional): Comma-separated list of languages to detect
            recursive (bool, optional): Whether to search recursively in directories
            
        Returns:
            Operation result with language statistics for each file and aggregated stats
        """
        try:
            # Convert boolean parameters if they're strings
            if isinstance(ignore_comments, str):
                ignore_comments = ignore_comments.lower() in ('true', 'yes', 'y', '1')
                
            if isinstance(recursive, str):
                recursive = recursive.lower() in ('true', 'yes', 'y', '1')
            
            # Convert min_word_length to integer if it's a string
            if isinstance(min_word_length, str):
                try:
                    min_word_length = int(min_word_length)
                except ValueError:
                    return {
                        "success": False,
                        "error": f"min_word_length must be an integer, received: {min_word_length}"
                    }
            
            # Parse the languages parameter if provided
            lang_list = None
            if languages:
                if isinstance(languages, str):
                    if languages.lower() == 'null' or languages.lower() == 'none':
                        lang_list = None
                    else:
                        lang_list = [lang.strip().lower() for lang in languages.split(',')]
                elif isinstance(languages, list):
                    lang_list = [lang.lower() for lang in languages]
                    
            # Load function words dictionaries
            function_words = self._load_function_words(lang_list)
            
            if not function_words:
                return {
                    "success": False,
                    "error": "No function word dictionaries could be loaded"
                }
                
            # Find files matching the pattern
            matching_files = self._find_files(file_path, recursive)
            
            if not matching_files:
                return {
                    "success": False,
                    "error": f"No files found matching the pattern: {file_path}"
                }
                
            # Analyze each file
            file_results = []
            
            for file_path in matching_files:
                result = self._analyze_file(file_path, ignore_comments, min_word_length, function_words)
                file_results.append(result)
                
            # Count successful analyses
            successful_analyses = [result for result in file_results if result.get('success', False)]
            
            if not successful_analyses:
                return {
                    "success": False,
                    "error": "No files could be successfully analyzed",
                    "file_results": file_results
                }
                
            # Aggregate results from all files
            aggregate_stats = {
                "total_files": len(matching_files),
                "analyzed_files": len(successful_analyses),
                "total_words": sum(result.get('total_words', 0) for result in successful_analyses),
                "language_counts": {},
                "language_percentages": {}
            }
            
            # Count words per language across all files
            language_totals = defaultdict(int)
            all_determined_words = 0
            
            for result in successful_analyses:
                for lang in function_words.keys():
                    word_count = result.get(f"{lang}_words", 0)
                    language_totals[lang] += word_count
                    all_determined_words += word_count
            
            # Calculate aggregate percentages
            if all_determined_words > 0:
                for lang, count in language_totals.items():
                    aggregate_stats["language_counts"][lang] = count
                    aggregate_stats["language_percentages"][lang] = round((count / all_determined_words) * 100, 2)
                    
                # Determine primary language in aggregate
                primary_lang = max(language_totals.items(), key=lambda x: x[1])
                if primary_lang[1] > 0:
                    aggregate_stats["primary_language"] = primary_lang[0].capitalize()
                else:
                    aggregate_stats["primary_language"] = "Undetermined"
            else:
                aggregate_stats["primary_language"] = "Undetermined"
                
            # Build a summary message
            if len(matching_files) == 1:
                # Single file analysis
                file_result = successful_analyses[0]
                
                summary_parts = []
                for lang, percent in file_result.get("language_stats", {}).items():
                    if lang != "undetermined_percent" and percent > 0:
                        lang_name = lang.replace("_percent", "").capitalize()
                        summary_parts.append(f"{percent}% {lang_name}")
                
                if summary_parts:
                    summary = f"File contains approximately {', '.join(summary_parts)} content."
                else:
                    summary = "Unable to determine language content."
            else:
                # Multiple files summary
                summary_parts = []
                for lang, percent in aggregate_stats["language_percentages"].items():
                    if percent > 0:
                        lang_name = lang.capitalize()
                        summary_parts.append(f"{percent}% {lang_name}")
                
                if summary_parts:
                    summary = f"Analyzed {len(successful_analyses)} files containing approximately {', '.join(summary_parts)} content."
                else:
                    summary = f"Analyzed {len(successful_analyses)} files but unable to determine language content."
            
            # Prepare the final result
            return {
                "success": True,
                "files_analyzed": len(successful_analyses),
                "total_files_matched": len(matching_files),
                "file_pattern": file_path,
                "aggregate_stats": aggregate_stats,
                "file_results": file_results,
                "summary": summary
            }
            
        except Exception as e:
            return {
                "success": False,
                "file_pattern": file_path,
                "error": str(e)
            } 