
from validator import PhoneValidator
from validator import PhoneValidator
from validator import URLValidator
from validator import DateValidator
from validator import EmailValidator

def test_validators():
    phone = PhoneValidator("+2348032056789")
    date = DateValidator("01-02-2024")
    url = URLValidator("https://google.com")
    Email = EmailValidator("baliqees.oladunjoye@gmail.com")

    print(f"Phone: {phone.validate()}")
    print(f"Date: {date.validate()}")
    print(f"URL: {url.validate()}")
    print(f"Email: {Email.validate()}")
    
if __name__ == "__main__":
    test_validators()
