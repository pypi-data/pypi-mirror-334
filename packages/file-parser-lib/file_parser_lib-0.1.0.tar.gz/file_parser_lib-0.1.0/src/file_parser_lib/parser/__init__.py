"""
Parser subpackage containing different file type parsers.
"""

from file_parser_lib.parser.file import FileParser
from file_parser_lib.parser.image import ImageParser
from file_parser_lib.parser.audio import AudioParser
from file_parser_lib.parser.unified_parser import UnifiedParser

__all__ = ["FileParser", "ImageParser", "AudioParser", "UnifiedParser"] 