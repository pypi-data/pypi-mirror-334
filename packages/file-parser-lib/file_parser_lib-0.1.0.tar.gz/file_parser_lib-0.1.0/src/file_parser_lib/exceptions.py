class FileParserException(Exception):
    """Base exception for file parser library"""
    pass

class DownloadError(FileParserException):
    """Raised when file download fails"""
    pass

class InvalidFileType(FileParserException):
    """Raised when file type is not supported"""
    pass

class ProcessingError(FileParserException):
    """Raised when file processing fails"""
    pass 