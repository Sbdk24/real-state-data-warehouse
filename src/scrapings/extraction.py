from typing import Optional, Union
import requests


def extraction(single_property, num_total_properties):
    # Iterating over them to get their specific information
    results = Extractor.get_hole_data(single_property, num_total_properties)

    return results


class Extractor:
    def __init__(self, property, num_total_properties) -> None:
        self.property = property
        self.headers = {"Accept": "*/*",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                        }
        self.num_total_properties = num_total_properties

    @classmethod
    def get_hole_data(cls, property_analized, num_total_properties) -> dict:
        instance = cls(property_analized, num_total_properties)

        amenties = instance.get_amenities()

        data = {
            "price": instance.get_price(),
            "currency": instance.get_currency(),
            "maintenance": instance.get_maintenance(),
            "location_p": instance.get_location(),
            "address_p": instance.get_address(),
            "meters": amenties[0],
            "rooms": amenties[1],
            "bathrooms": amenties[2],
            "parking_spaces": amenties[3],
            "link": instance.get_link(),
            "description_p": instance.get_description(),
            "image_p": instance.get_images()
        }

        return data

    def get_price(self) -> Optional[int]:
        # Clean and convert price to integer
        if price := self.extract_from_html('div', {'data-qa': 'POSTING_CARD_PRICE'}):
            # Extract price specifically and return it as integeer
            price = price.strip().removeprefix('MN').replace(',', '').replace(
                ' ', '').removeprefix('USD').lower()

            return None if 'consultar precio' in price else int(price)

        return None

    def get_currency(self) -> Optional[str]:
        if currency := self.extract_from_html('div', {'data-qa': 'POSTING_CARD_PRICE'}):
            # Determine currency based on prefix
            currency = 'MX' if 'MN' in currency else 'USD'

            return currency

        return None

    def get_maintenance(self) -> Optional[int]:
        if maintenance := self.extract_from_html('div', {'data-qa': 'expensas'}):
            # Clean and convert maintenance fee to integer, or set to None if not found
            maintenance = maintenance.strip().removeprefix('MN ').removeprefix(
                'USD ').removesuffix(' Mantenimiento').replace(',', '')

            return int(maintenance)

        return None  # Set to None if not found

    def get_location(self) -> Optional[int]:
        try:
            # Extract the neighborhood
            neighborhood = self.property.find(
                'div', class_='LocationBlock-sc-ge2uzh-1 cVCbkm')

            neighborhood = neighborhood.find('div')

            if not self.is_filled(neighborhood):
                return None

            neighborhood = neighborhood.text.strip().replace(
                '\'', '\'\'').replace('\"', '\"\"')

            return neighborhood
        except (AttributeError, TypeError):
            return None  # Set to None if not found

    def get_address(self) -> Optional[str]:
        if location := self.extract_from_html('h2', {'data-qa': 'POSTING_CARD_LOCATION'}):
            return ' '.join(location.replace('\n', '').split())

        return None

    def get_link(self) -> Optional[str]:
        try:
            value = self.property.find(
                'h3', attrs={'data-qa': 'POSTING_CARD_DESCRIPTION'}).a

            paragraph = value.get('href')

            link = "www.inmuebles24.com" + paragraph

            return link
        except (AttributeError, TypeError, ValueError):
            return None  # Set to False if not found

    def get_description(self) -> Optional[str]:
        if description := self.extract_from_html('h3', {'data-qa': 'POSTING_CARD_DESCRIPTION'}):
            # Escape single and double quotes
            description = description.replace(
                '\'', '\'\'').replace('\"', '\"\"')

            return description

        return None

    def get_amenities(self) -> list:
        # Extract the amenities
        try:
            amenities = ' '.join(span.get_text().replace('.', '') + ',' for span in self.property.find(
                # Join amenities into a string
                'h3', attrs={'data-qa': 'POSTING_CARD_FEATURES'})).removesuffix(',')
        except (AttributeError, TypeError):
            amenities = ''  # Set to None if not found

        return parse_property_info(amenities)

    def extract_from_html(self, tag, attributes):
        try:  # Extract the maintenance fee
            value = self.property.find(tag, attrs=attributes).text.strip()

            return value if self.is_filled(value) else False

        except (AttributeError, TypeError, ValueError):
            return False  # Set to False if not found

    def get_images(self) -> Optional[bytes]:
        try:
            image = self.property.find(
                'div', attrs={'data-qa': 'POSTING_CARD_GALLERY'}).img

            image_url = image.get('src')

            response = requests.request(
                "GET", image_url, data="",  headers=self.headers)
            return response.content
        except (AttributeError, TypeError, ValueError):
            return None  # Set to False if not found
        
    @staticmethod
    def is_filled(value) -> bool:
        return False if not value or value == '' else True

def parse_property_info(amenities) -> list:
    # Initialize variables to store the extracted values
    meters, rooms, bathrooms, parking_spaces = '', '', '', ''

    # Split the amenities string into a list of individual amenities
    cases = amenities.split(',')

    # Iterate through each individual amenity
    for case in cases:
        # Check if the amenity contains 'm²' and not ' a ' (space + 'a' + space)
        if 'm²' in case and ' a ' not in case:
            # Extract the numeric value before 'm² tot' and convert it to an integer
            meters = ' '.join(case.split())
            meters = int(meters.replace(
                ' m² tot', '').replace('\n', '').strip())

        # Check if the amenity contains 'rec' and not ' a '
        elif 'rec' in case and ' a ' not in case:
            # Extract the numeric value after 'rec' and convert it to an integer
            rooms = int(case.replace('rec', '').strip())

        # Check if the amenity contains 'baño' and not ' a '
        elif 'baño' in case and ' a ' not in case:
            # Extract the numeric value after 'baños' or 'baño' and convert it to an integer
            bathrooms = int(case.replace(
                'baños', '').replace('baño', '').strip())

        # Check if the amenity contains 'esta' and not ' a '
        elif 'esta' in case and ' a ' not in case:
            # Extract the numeric value after 'estac' and convert it to an integer
            parking_spaces = int(case.replace('estac', '').strip())

    # Return a list with the extracted values or None if no value was found
    return [meters or None, rooms or None, bathrooms or None, parking_spaces or None]
