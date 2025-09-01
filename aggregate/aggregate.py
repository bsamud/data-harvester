"""Aggregate data from multiple sources"""
import json
import pandas as pd
from pathlib import Path
from common.logger import log

class DataAggregator:
    """Aggregate and combine data from various sources"""

    def __init__(self):
        self.data_frames = []

    def load_json_files(self, file_paths):
        """Load multiple JSON files"""
        data = []

        for file_path in file_paths:
            try:
                with open(file_path, 'r') as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        data.extend(content)
                    else:
                        data.append(content)
            except Exception as e:
                log.error(f"Error loading {file_path}: {e}")

        log.info(f"Loaded {len(data)} records from {len(file_paths)} files")
        return data

    def json_to_dataframe(self, json_data):
        """Convert JSON data to DataFrame"""
        try:
            df = pd.json_normalize(json_data)
            log.info(f"Created DataFrame: {df.shape}")
            return df
        except Exception as e:
            log.error(f"Error creating DataFrame: {e}")
            return None

    def aggregate_directory(self, directory, pattern='*.json'):
        """Aggregate all JSON files in directory"""
        file_paths = list(Path(directory).rglob(pattern))
        data = self.load_json_files(file_paths)

        return self.json_to_dataframe(data)

    def merge_dataframes(self, dataframes, on=None, how='outer'):
        """Merge multiple DataFrames"""
        if not dataframes:
            return None

        result = dataframes[0]

        for df in dataframes[1:]:
            result = pd.merge(result, df, on=on, how=how)

        log.info(f"Merged {len(dataframes)} DataFrames: {result.shape}")
        return result
