import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import re
from datetime import datetime, date
from src.logic.countries_logic import CountryLogic
from src.logic.vacations_logic import VacationLogic


class VacationFacade:
    def __init__(self):
        self.params = []
        self.now = date.today()
        self.logic = VacationLogic()
        self.country_logic = CountryLogic()

    def add_vacation(self):
        self.get_title()
        self.get_description()
        self.get_start_date()
        self.get_end_date()
        self.get_countries_name()
        self.get_price()
        self.get_image()

        return self.logic.add_vacation(*self.params)

    def get_title(self):
        while True:
            title = input("Enter title: ").strip()
            if not title.replace(" ", "").isalpha():
                print("Title must contain only letters and spaces")
            elif len(title) < 5:
                print("Title must be at least 5 characters long")
            else:
                self.params.append(title)
                print("Title added")
                break

    def get_countries_name(self):
        while True:
            countries_name = input("Enter country name: ").lower()
            if self.country_logic.check_if_country_exists(countries_name):
                print("Country added to vacation info!")
                self.params.append(countries_name)
                break
            else:
                print(
                    "Country does not exist in database, here is a list of all countries:")
                countries = self.country_logic.get_all_countries()
                print(" | ".join(country["country_name"]
                      for country in countries))

    def get_description(self):
        while True:
            description = input("Enter description: ").strip()
            if not description:
                print("Description is mandatory!")
            else:
                self.params.append(description)
                break

    def get_start_date(self):

        while True:
            try:
                date_str = input("Enter start date (YYYY-MM-DD): ")
                start_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                if start_date < self.now:
                    print("Start date cannot be in the past")
                    continue

                self.params.append(start_date)
                print("Start date added")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")

    def get_end_date(self):

        while True:
            try:
                date_str = input("Enter end date (YYYY-MM-DD): ")
                end_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                if end_date < self.now:
                    print("End date cannot be in the past")
                    continue

                if end_date <= self.params[-1]:  
                    print("End date must be after start date")
                    continue

                self.params.append(end_date)
                print("End date added")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")

    def get_price(self):
        while True:
            try:
                price = float(input("Enter price: "))
                if not 1000 <= price <= 10000:
                    print("Price must be between 1000 and 10000")
                else:
                    self.params.append(price)
                    print("Price added")
                    break
            except ValueError:
                print("Price must be a number!")

    def get_image(self):
        while True:
            image_url = input(
                "Enter image URL (optional, press Enter to skip): ").strip()
            if not image_url:
                self.params.append(None)
                print("No image URL selected")
                break

            # Basic URL validation with regular expression
            url_pattern = r'^https?:\/\/[^\s\/$.?#].[^\s]*$'
            if not re.match(url_pattern, image_url):
                print("Invalid URL format!")
                continue

            self.params.append(image_url)
            print("Image URL added")
            break


if __name__ == "__main__":

    vacation = VacationFacade()

    result = vacation.add_vacation()

    print("\nBooking Results:")
    print("---------------")
    print(f"Vacation title: {vacation.params[0]}")
    print(f"Description: {vacation.params[1]}")
    print(f"Start date: {vacation.params[2]}")
    print(f"End date: {vacation.params[3]}")
    print(f"Country: {vacation.params[4]}")
    print(f"Price: ${vacation.params[5]}")
    print(f"Image URL: {vacation.params[6]}")