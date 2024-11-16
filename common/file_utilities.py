"""File utilities including hashing for delta detection"""
import hashlib
import json
import os
from pathlib import Path
from common.logger import log

def calculate_md5(file_path):
    """
    Calculate MD5 hash of file

    Args:
        file_path: Path to file

    Returns:
        str: MD5 hash hex string
    """
    hash_md5 = hashlib.md5()

    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        log.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        log.error(f"Error calculating hash: {e}")
        return None

def load_hash_data(hash_file):
    """Load hash data from JSON file"""
    if not os.path.exists(hash_file):
        return {}

    try:
        with open(hash_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        log.error(f"Invalid JSON in hash file: {hash_file}")
        return {}

def save_hash_data(hash_file, hash_data):
    """Save hash data to JSON file"""
    os.makedirs(os.path.dirname(hash_file), exist_ok=True)

    with open(hash_file, 'w') as f:
        json.dump(hash_data, f, indent=2)

def has_file_changed(file_path, hash_data):
    """Check if file has changed based on MD5 hash"""
    current_hash = calculate_md5(file_path)
    if current_hash is None:
        return True

    file_key = str(file_path)
    previous_hash = hash_data.get(file_key)

    return current_hash != previous_hash
