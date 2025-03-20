"""
file_parser_lib - A library for parsing various file types.

This library provides parsers for different file types including images and audio files.
"""

__version__ = "0.1.0"

# Import main components to make them available at the package level
from file_parser_lib.parser.file import FileParser
from file_parser_lib.parser.image import ImageParser
from file_parser_lib.parser.audio import AudioParser
from file_parser_lib.parser.unified_parser import UnifiedParser

__all__ = ["FileParser", "ImageParser", "AudioParser", "UnifiedParser"] 