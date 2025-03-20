import re
from datetime import datetime

class DataValidator:
    """A class to validate emails, phone numbers, dates, and URLs."""

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validates an email address and returns a descriptive message.

        - Supports:
          - Standard email format (e.g., "user@example.com").
        - Rejects:
          - Missing '@' or domain (e.g., "userexample.com").
          - Invalid characters.
          - Domains without extensions (e.g., "user@domain").
          - Too short or too long emails.
        
        :param email: The email address to validate.
        :return: A message indicating validity or the reason for invalidity.
        """
        if not email.strip():
            return "Email field cannot be empty."
                
        if len(email) > 320:
            return "Email is too long. It must not exceed 320 characters."
        
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email):
            return "Invalid email format. Ensure it follows the pattern 'example@domain.com'."
        
        return "Valid email address."

    @staticmethod
    def validate_phone(phone: str) -> str:
        """
        Validates phone numbers and returns a descriptive message.

        - Supports:
          - International format (e.g., +2348012345678, +12345678901).
          - Nigerian local format (e.g., 08012345678).
        - Rejects:
          - Missing country code (if international).
          - Incorrect number length.
        
        :param phone: The phone number to validate.
        :return: A message indicating validity or the reason for invalidity.
        """
        if not phone.strip():
            return "Phone number cannot be empty."

        phone_pattern = r"^\+?\d{7,15}$"  # Supports international format +1234567890
        if not re.match(phone_pattern, phone):
            return "Invalid phone number format. Use a valid local or international format."
        
        return "Valid phone number!"

    @staticmethod
    def validate_date(date: str) -> str:
        """
        Validates a date in DD/MM/YYYY format and returns a descriptive message.

        - Ensures day (01-31) fits the month.
        - Enforces a four-digit year.
        
        :param date: The date string to validate.
        :return: A message indicating validity or the reason for invalidity.
        """
        if not date.strip():
            return "Date field cannot be empty."

        date_pattern = r"^\d{2}/\d{2}/\d{4}$"
        if not re.match(date_pattern, date):
            return "Invalid date format."

        try:
            day, month, year = map(int, date.split('/'))
            datetime(year, month, day)  # Validates real dates
            return "Valid date"
        except ValueError:
            return "Invalid date format."

    @staticmethod
    def validate_url(url: str) -> str:
        """
        Validates a URL and returns a descriptive message.

        - Supports:
          - "http://", "https://", and "www." formats.
          - Valid domains with extensions (.com, .org, .net, .co.uk, etc.).
          - URLs with paths, query parameters, and ports.
        - Rejects:
          - URLs missing a domain extension (e.g., "https://google").
          - Invalid characters in the domain.

        :param url: The URL to validate.
        :return: A message indicating validity or the reason for invalidity.
        """
        if not url.strip():
            return "URL field cannot be empty."

        url_pattern = (
            r"^(https?:\/\/)?"  # Optional http or https
            r"(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6})"  # Domain name
            r"(:\d{1,5})?"  # Optional port
            r"(\/[^\s]*)?$"  # Optional path
        )
        if not re.match(url_pattern, url):
            return "Invalid URL format. Ensure it starts with 'http://' or 'https://'."
        
        return "Valid URL."




if __name__ == "__main__":
    validator = DataValidator()

    while True:
        print("\nSelect the type of data to validate:")
        print("1. Email")
        print("2. Phone Number")
        print("3. Date (DD/MM/YYYY)")
        print("4. URL")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            email = input("Enter an email address: ")
            print(validator.validate_email(email))

        elif choice == "2":
            phone = input("Enter a phone number: ")
            print(validator.validate_phone(phone))

        elif choice == "3":
            date = input("Enter a date (DD/MM/YYYY): ")
            print(validator.validate_date(date))

        elif choice == "4":
            url = input("Enter a URL: ")
            print(validator.validate_url(url))

        elif choice == "5":
            print("Exiting program. Goodbye! 👋👋👋")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5.")
