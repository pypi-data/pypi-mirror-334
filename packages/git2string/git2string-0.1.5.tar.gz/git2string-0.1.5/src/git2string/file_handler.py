import os
from urllib.parse import urlparse


class FileHandler:
    def __init__(self, include_binary=False):
        """Initialize with a flag for including binary files."""
        self.include_binary = include_binary

    @staticmethod
    def is_binary(filename):
        """Very basic check if a file might be binary."""
        try:
            with open(filename, "rb") as f:
                test = f.read(1024)
                if b"\0" in test:
                    return True
        except:
            pass
        return False

    @staticmethod
    def is_url(string):
        """
        Check if the repo location is a URL.
        """
        try:
            result = urlparse(string)
            return True if all([result.scheme, result.netloc]) else False
        except ValueError:
            return False

    def read_file(self, file_path):
        """Read and return file content, handling binary if specified."""
        try:
            with open(file_path, "r", encoding="utf-8") as infile:
                return infile.read()
        except UnicodeDecodeError:
            if self.include_binary:
                with open(file_path, "rb") as infile:
                    return infile.read().hex()
        return None
