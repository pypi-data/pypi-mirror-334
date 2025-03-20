import re
from datetime import datetime


class DataValidator:        #creating a parent class DataValidator
    def __init__ (self):
        pass

    def validate(self, data):     #creating a method "validate"
        raise NotImplementedError ("Subclasses must implement this method")


class EmailValidator(DataValidator):
    #inheriting the parent class "DataValidator"
    def __init__ (self, email):
        super().__init__ ()
        self.email = email

    def validate(self):
        #overriding the method in the parent class
        pattern = r'[\w\.-]+@[\w\.-]+\.+\w+$'
        if re.match(pattern, self.email):
            return "valid email"
        else:
            return "invalid email"

class PhoneValidator(DataValidator):
    def __init__ (self, phone_number):
        super().__init__ ()
        self.phone_number = phone_number

    def validate (self):
        #Defining a regex pattern for Nigeria phone number validation
        pattern = r'^(\+234|234|0)?[7-9][0-1]\d{8}$'
        if re.match(pattern, self.phone_number):
            return "valid phone number"
        else:
            return "invalid phone number"
            
class DateValidator(DataValidator): 
    def __init__(self, date):
        super().__init__()
        self.date = date

    def validate(self):
        # Regex pattern to match YYYY-MM-DD, DD-MM-YYYY, MM-DD-YYYY (with - or /)
        # STRICT regex: Ensures MM and DD are exactly 2 digits
        pattern = r'^(?:\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})$'
        if not re.fullmatch(pattern, self.date):
            return "Invalid date format"

        # Possible formats to check
        possible_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"]

        # Validate by attempting to parse with each format
        for fmt in possible_formats:
            try:
                datetime.strptime(self.date, fmt)
                return "Valid date"
            except ValueError:
                continue  # Try the next format

        return "Invalid date"
    

class URLValidator(DataValidator):
    def __init__ (self, url):
        super().__init__ ()
        self.url = url

    def validate (self):
        #Defining a regex pattern for URL validation
        pattern = r'^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/[\w\-.,@?^=%&:/~+#]*)?$'

        if re.match(pattern, self.url):
            return "Valid URL"
        else:
            return "Invalid URL"
           