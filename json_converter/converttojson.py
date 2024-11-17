"""Convert various formats to JSON"""
import json
import xmltodict
from common.logger import log

def xml_to_json(xml_string):
    """
    Convert XML string to JSON

    Args:
        xml_string: XML content as string

    Returns:
        dict: Parsed JSON data
    """
    try:
        data = xmltodict.parse(xml_string)
        return data
    except Exception as e:
        log.error(f"XML parsing error: {e}")
        return None

def save_as_json(data, output_file):
    """
    Save data as JSON file

    Args:
        data: Data to save
        output_file: Output file path
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        log.info(f"Saved JSON to {output_file}")
        return True
    except Exception as e:
        log.error(f"Error saving JSON: {e}")
        return False
