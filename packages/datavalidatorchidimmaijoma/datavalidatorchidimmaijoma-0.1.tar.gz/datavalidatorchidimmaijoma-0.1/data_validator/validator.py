import re #Regular Expression module to be used for validations
from datetime import datetime #Date Time module to validate dates
from urllib.parse import urlparse #URL Library module to validate urls

class DataValidator:
    """
    A class for validating personal data entries such as emails, phone numbers, dates, and URLs.
    """

    def validate_email(self, email):
        """
        Validates if the provided string is a valid email address.

        Parameters:
            email (str): The email address to validate.

        Returns:
            bool: True if valid, False if not.
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Regular expression pattern for validating email
        return bool(re.match(pattern, email))

    def validate_phone(self, phone):
        """
        Validates if the provided string is a valid phone number.

        Parameters:
            phone (str): The phone number to validate.

        Returns:
            bool: True if valid, False if not.
        """
        pattern = r'^\+?\d{10,15}$'  # Regular expression pattern for validating local or international phone numbers(begin with a + sign)
        return bool(re.match(pattern, phone))

    def validate_date(self, date_str, date_format="%d-%m-%Y"):
        """
        Validates if the provided string matches the given date format.

        Parameters:
            date_str (str): The date string to validate.
            date_format (str): The expected format of the date string. Default is '%d-%m-%Y'(DD-MM-YYYY).

        Returns:
            bool: True if valid, False if not.
        """
        try:
            datetime.strptime(date_str, date_format)  # Attempt to parse the date string
            return True
        except ValueError:
            return False

    def validate_url(self, url):
        """
        Validates if the provided string is a valid URL.

        Parameters:
            url (str): The URL string to validate.

        Returns:
            bool: True if valid, False if not.
        """
        result = urlparse(url)  # Parse the URL to check its components
        return all([result.scheme, result.netloc])  # Ensure URL has both scheme and network location
