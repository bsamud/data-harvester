"""Delta detection for identifying changed files"""
import os
from common.file_utilities import calculate_md5, load_hash_data, save_hash_data, has_file_changed
from common.logger import log

class DeltaDetector:
    """Detect changes in files using MD5 hashing"""

    def __init__(self, hash_file='hashes.json'):
        self.hash_file = hash_file
        self.hash_data = load_hash_data(hash_file)
        self.new_files = []
        self.modified_files = []
        self.unchanged_files = []

    def scan_directory(self, directory, file_pattern='*'):
        """
        Scan directory for changes

        Args:
            directory: Directory to scan
            file_pattern: File pattern to match

        Returns:
            dict: Delta detection results
        """
        from pathlib import Path

        self.new_files = []
        self.modified_files = []
        self.unchanged_files = []

        files = list(Path(directory).rglob(file_pattern))

        for file_path in files:
            if not file_path.is_file():
                continue

            file_str = str(file_path)

            # Check if file is new or modified
            if file_str not in self.hash_data:
                self.new_files.append(file_str)
                self.hash_data[file_str] = calculate_md5(file_str)
            elif has_file_changed(file_str, self.hash_data):
                self.modified_files.append(file_str)
                self.hash_data[file_str] = calculate_md5(file_str)
            else:
                self.unchanged_files.append(file_str)

        log.info(f"Delta detection: {len(self.new_files)} new, "
                f"{len(self.modified_files)} modified, "
                f"{len(self.unchanged_files)} unchanged")

        return {
            'new': self.new_files,
            'modified': self.modified_files,
            'unchanged': self.unchanged_files
        }

    def save_hashes(self):
        """Save current hash data"""
        save_hash_data(self.hash_file, self.hash_data)
        log.info(f"Saved hashes to {self.hash_file}")
