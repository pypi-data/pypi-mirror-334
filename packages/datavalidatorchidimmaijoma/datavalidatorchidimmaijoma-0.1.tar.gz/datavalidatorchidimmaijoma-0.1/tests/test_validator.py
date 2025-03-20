import unittest #Testing module for the package
import sys #A module to interact with system-specific parameters
import os #A module to interact with files and directories

# Adding the parent directory of the package 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_validator.validator import DataValidator

class TestDataValidator(unittest.TestCase):
    """
    Test class for the DataValidator methods.
    """

    def setUp(self):
        """
        Setup method to create an instance of DataValidator before each test.
        """
        self.validator = DataValidator()

    def test_validate_email(self):
        """
        Test the validate_email method with valid and invalid email addresses.
        """
        self.assertTrue(self.validator.validate_email("test@example.com"))  # Valid email
        self.assertFalse(self.validator.validate_email("invalid-email"))    # Invalid email

    def test_validate_phone(self):
        """
        Test the validate_phone method with valid and invalid phone numbers.
        """
        self.assertTrue(self.validator.validate_phone("+1234567890"))  # Valid international number
        self.assertFalse(self.validator.validate_phone("123-456"))     # Invalid phone format

    def test_validate_date(self):
        """
        Test the validate_date method with valid and invalid dates.
        """
        self.assertTrue(self.validator.validate_date("12-03-2025"))   # Valid date
        self.assertFalse(self.validator.validate_date("2025-03-12")) # Invalid format

    def test_validate_url(self):
        """
        Test the validate_url method with valid and invalid URLs.
        """
        self.assertTrue(self.validator.validate_url("https://example.com"))  # Valid URL
        self.assertFalse(self.validator.validate_url("example.com"))         # Invalid URL (missing scheme)

if __name__ == "__main__":
    unittest.main()  # Run the unit tests
