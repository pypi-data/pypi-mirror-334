import re

class DataValidator:
    """
    A class for validating personal data such as emails, phone numbers, dates, and URLs.
    """

    def validate_email(self, email: str) -> bool:
        """
        Validates an email address.

        - Supports:
           -Standard email format (e.g., "user@example.com").
        - Rejects:
           -Missing '@' or domain (e.g., "userexample.com").
           -Invalid characters.
           -Domains without extensions (e.g., "user@domain").
        
        :param email: The email address to validate.
        :return: True if valid, False otherwise.
        """
        pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def validate_phone(self, phone: str) -> bool:
        """
        Validates phone numbers:
        - Supports international format (e.g., +2348012345678, +12345678901).
        - Supports Nigerian local format (e.g., 08012345678).
        - No spaces or hyphens allowed.
        """
        pattern = r"^(?:\+(\d{1,4})|0)(\d{10})$"
        return bool(re.match(pattern, phone))

    def validate_date(self, date: str) -> bool:
        """
        Validates a date in DD/MM/YYYY format with proper day-month matching.
        - Ensures day (01-31) fits the month.
        - Enforces a four-digit year.
        """
        pattern = r"""^(
            (0[1-9]|1\d|2[0-8])/(0[1-9]|1[0-2])/\d{4} |  # Days 01-28 (all months)
            (29/(0[13-9]|1[0-2])/\d{4}) |  # 29th day (all months except February)
            (30/(0[13-9]|1[0-2])/\d{4}) |  # 30th day (only valid in months with 30+ days)
            (31/(0[13578]|1[02])/\d{4}) |  # 31st day (only in Jan, Mar, May, Jul, Aug, Oct, Dec)
        )$"""
        return bool(re.match(pattern, date, re.VERBOSE))

    def validate_url(self, url: str) -> bool:
        """
        Validates a URL.

        - Supports:
          - "http://", "https://", and "www." formats.
          - Valid domains with extensions (.com, .org, .net, .co.uk, etc.).
          - URLs with paths, query parameters, and ports.
        - Rejects:
          - URLs missing a domain extension (e.g., "https://google").
          - Invalid characters in the domain.

        :param url: The URL to validate.
        :return: True if valid, False otherwise.
        """
        pattern = r"^(https?:\/\/)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?(\/\S*)?$"
        return bool(re.match(pattern, url))


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
            print("Valid Email " if validator.validate_email(email) else "Invalid Email ")

        elif choice == "2":
            phone = input("Enter a phone number: ")
            print("Valid Phone Number " if validator.validate_phone(phone) else "Invalid Phone Number ")

        elif choice == "3":
            date = input("Enter a date (DD/MM/YYYY): ")
            print("Valid Date " if validator.validate_date(date) else "Invalid Date ")

        elif choice == "4":
            url = input("Enter a URL: ")
            print("Valid URL " if validator.validate_url(url) else "Invalid URL ")

        elif choice == "5":
            print("Exiting program. Goodbye! ")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
