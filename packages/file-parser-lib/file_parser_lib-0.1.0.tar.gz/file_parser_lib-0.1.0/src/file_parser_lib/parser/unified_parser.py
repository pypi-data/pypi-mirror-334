"""
UnifiedParser - A parser that automatically selects the appropriate parser based on file type.
"""

import os
import mimetypes
from typing import Dict, Any, Optional

from file_parser_lib.parser.file import FileParser
from file_parser_lib.parser.image import ImageParser
from file_parser_lib.parser.audio import AudioParser


class UnifiedParser:
    """
    A unified parser that automatically selects the appropriate parser based on file type.
    """

    def __init__(self, file_path: str):
        """
        Initialize the UnifiedParser with a file path.

        Args:
            file_path (str): Path to the file to be parsed
        """
        self.file_path = file_path
        self._parser = self._get_appropriate_parser()

    def _get_appropriate_parser(self):
        """
        Determine the appropriate parser based on file extension and/or mime type.

        Returns:
            The appropriate parser instance (FileParser, ImageParser, or AudioParser)
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        # Get file extension and mime type
        _, ext = os.path.splitext(self.file_path)
        ext = ext.lower()
        mime_type, _ = mimetypes.guess_type(self.file_path)

        # Image file extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        
        # Audio file extensions
        audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a']

        # Check mime type first
        if mime_type:
            if mime_type.startswith('image/'):
                return ImageParser(self.file_path)
            elif mime_type.startswith('audio/'):
                return AudioParser(self.file_path)
        
        # Fall back to extension check
        if ext in image_extensions:
            return ImageParser(self.file_path)
        elif ext in audio_extensions:
            return AudioParser(self.file_path)
        
        # Default to generic file parser
        return FileParser(self.file_path)

    def parse(self) -> Dict[str, Any]:
        """
        Parse the file using the appropriate parser.

        Returns:
            Dict[str, Any]: Parsed data from the file
        """
        return self._parser.parse()
    
    @property
    def parser_type(self) -> str:
        """
        Get the type of parser being used.

        Returns:
            str: The type of parser ('file', 'image', or 'audio')
        """
        if isinstance(self._parser, ImageParser):
            return 'image'
        elif isinstance(self._parser, AudioParser):
            return 'audio'
        else:
            return 'file' 