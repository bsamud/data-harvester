"""XML to JSON conversion"""
import xmltodict
import json
from common.logger import log

class XMLConverter:
    """Convert XML files to JSON"""

    def __init__(self):
        self.converted_count = 0

    def convert_file(self, xml_file, json_file):
        """
        Convert XML file to JSON file

        Args:
            xml_file: Input XML file path
            json_file: Output JSON file path

        Returns:
            bool: Success status
        """
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            # Parse XML
            data = xmltodict.parse(xml_content)

            # Save as JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.converted_count += 1
            log.info(f"Converted {xml_file} to {json_file}")
            return True

        except Exception as e:
            log.error(f"Conversion error: {e}")
            return False

    def batch_convert(self, xml_files, output_dir):
        """Convert multiple XML files"""
        import os

        os.makedirs(output_dir, exist_ok=True)

        for xml_file in xml_files:
            filename = os.path.basename(xml_file)
            json_filename = filename.replace('.xml', '.json')
            json_file = os.path.join(output_dir, json_filename)

            self.convert_file(xml_file, json_file)

        log.info(f"Batch conversion completed: {self.converted_count} files")
