import re

class DataValidator:
    """
    A data validation class for validating various types of inputs.
    
    Methods:
        validate_email() - Validates email addresses.
        validate_phone() - Validates phone numbers.
        validate_date()  - Validates date strings in multiple formats.
        validate_url()   - Validates URLs.
    """
    
    def __init__(self, data=None, verbose=False):
        self.data = data
        self.verbose = verbose
        """
        Initializes the DataValidator object with optional data and verbosity.
        
        Parameters:
            data (str): The data to be validated. Defaults to None.
            verbose (bool): If True, provides detailed validation messages. Defaults to False.
        """

    def validate_email(self):
        """
        Validates an email address using a regular expression pattern.
        
        Returns:
            bool: True if the email address is valid, False otherwise.
            str (optional): A message indicating the validation status if verbosity is enabled.
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        is_valid = bool(re.match(pattern, self.data))
        
        if self.verbose:
            if is_valid:
                return True, f"Valid email address: {self.data}"
            else:
                return False, f"Invalid email address: {self.data}"
        
        return is_valid

    def validate_phone(self):
        """
        Validates a phone number using the E.164 format.
        
        Returns:
            bool: True if the phone number is valid, False otherwise.
            str (optional): A message indicating the validation status if verbosity is enabled.
        """
        pattern = r'^\+?[1-9]\d{1,14}$'
        is_valid = bool(re.match(pattern, self.data))
        
        if self.verbose:
            if is_valid:
                return True, f"Valid phone number: {self.data}"
            else:
                return False, f"Invalid phone number: {self.data}"
        
        return is_valid

    def validate_date(self):
        """
        Validates a date string in multiple formats, including support for:
        - YYYY-MM-DD
        - YYYY/MM/DD
        - Leap years for February (including support for 28 and 29 days)
        - Proper handling of months with 30 and 31 days
        
        Returns:
            bool: True if the date string is valid, False otherwise.
            str (optional): A message indicating the validation status if verbosity is enabled.
        """
        pattern = r'^(\d{1,4})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])$'
        match = re.match(pattern, self.data)
        
        if not match:
            if self.verbose:
                return False, f"Invalid date format: {self.data}"
            return False
        
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        
        # Check for valid days in February (leap year support)
        """
        if day > 29
            This checks if the given day is more than 29 (which is impossible even in a leap year),
            It then returns false, which shows that the date is invalid.
        day == 29
            Checks if the day is 29 (the leap day).
        (year % 4 != 0)
            Checks if the year is not divisible by 4 (not a leap year).
            If true, the date is invalid.
        (year % 100 == 0 and year % 400 != 0)
            Checks for century years (like 1900, 2000).
            If the year is divisible by 100 but not divisible by 400, it's not a leap year
        """
        if month == 2:
            if day > 29 or (day == 29 and (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0))):
                if self.verbose:
                    return False, f"Invalid date for February: {self.data}"
                return False
        
        # Check for months with 30 days
        if month in [4, 6, 9, 11] and day > 30:
            if self.verbose:
                return False, f"Invalid day for month {month}: {self.data}"
            return False
        
        if self.verbose:
            return True, f"Valid date: {self.data}"
        
        return True

    def validate_url(self):
        """
        Validates a URL string using comprehensive URL formats.
        Returns:
            bool: True if the URL is valid, False otherwise.
            str (optional): A message indicating the validation status if verbosity is enabled.
        """
        # Comprehensive regex pattern for various URL formats
        pattern = (
            r'^[a-zA-Z][a-zA-Z\d+.-]*://'       # Protocol (http, https, ftp, ws, mailto, and others.)
            r'((\w+:\w+@)?'                     # Optional username:password@
            r'([a-zA-Z\d.-]+|\[[a-fA-F\d:.]+\])' # Domain name or IPv4/IPv6 address
        )

        is_valid = bool(re.match(pattern, self.data))

        if self.verbose:
            if is_valid:
                return True, f"Valid URL: {self.data}"
            else:
                return False, f"Invalid URL: {self.data}"

        return is_valid

