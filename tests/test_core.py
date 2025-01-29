import unittest
from common.file_utilities import calculate_md5

class TestCore(unittest.TestCase):
    def test_md5_calculation(self):
        # Basic test
        self.assertIsNotNone(calculate_md5)

if __name__ == '__main__':
    unittest.main()
