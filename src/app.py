from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()
"""
Headers are a useful piece of information extracted your own 
credentials for letting the page 'knowyou're a human. 

You can find them opening the browser console and typing navigator.userAgent
"""

headers = {'User-Agent': os.getenv('HEADER')}

states = [
    {'url_key': 'ciudad-de-mexico', 'filename': 'cdmx', 'name': 'ciudad de mexico'},
    {'url_key': 'edo.-de-mexico', 'filename': 'est_mx', 'name': 'estado de mexico'},
    {'url_key': 'queretaro-provincia', 'filename': 'queretaro', 'name': 'queretaro'},
    {'url_key': 'morelos-provincia', 'filename': 'morelos', 'name': 'morelos'},
    {'url_key': 'nuevo-leon', 'filename': 'nuevo_leon', 'name': 'nuevo leon'},
    {'url_key': 'yucatan', 'filename': 'yucatan', 'name': 'yucatan'},
    {'url_key': 'quintana-roo', 'filename': 'quintana_roo', 'name': 'quintana roo'},
    {'url_key': 'jalisco', 'filename': 'jalisco', 'name': 'jalisco'},
    {'url_key': 'veracruz-provincia', 'filename': 'veracruz', 'name': 'veracruz'},
    {'url_key': 'puebla-provincia', 'filename': 'puebla', 'name': 'puebla'},
    {'url_key': 'hidalgo-provicia', 'filename': 'hidalgo', 'name': 'hidalgo'},
    {'url_key': 'guerrero-provincia', 'filename': 'guerrero', 'name': 'guerrero'},
    {'url_key': 'san-luis-potosi-provincia', 'filename': 'sl_potosi', 'name': 'san luis potosi'},
    {'url_key': 'coahuila', 'filename': 'coahuila', 'name': 'coahuila'},
    {'url_key': 'durango-provincia', 'filename': 'durango', 'name': 'durango'},
    {'url_key': 'guanajuato-provincia', 'filename': 'guanajuato', 'name': 'guanajuato'},
    {'url_key': 'chiapas', 'filename': 'chiapas', 'name': 'chiapas'},
    {'url_key': 'chihuahua-provincia', 'filename': 'chihuahua', 'name': 'chihuahua'},
    {'url_key': 'tamaulipas', 'filename': 'tamaulipas', 'name': 'tamaulipas'},
    {'url_key': 'baja-california-norte', 'filename': 'bc_norte', 'name': 'baja california norte'}
]


def main():
    for state in states:
        for i in range(1000):
            # Url for inm24 current web page
            url = f'https://www.inmuebles24.com/inmuebles-en-venta-en-{state['url_key']}-pagina-{i + 1}.html'
            html = get_status(url)
            
            # Start using BeautifulSoup with lxml which is currently the best parser
            """
            A parser is an HTML analizer who allow us to process and manipulate 
            XML and HTML text very efficiently and high performance.
            """
            if html:
                # Strart scraping all the properties we have on this particular page
                # There're always 20 per page
                inm24 = BeautifulSoup(html.text, 'lxml')
                properties = inm24.find_all('div', class_='sc-1tt2vbg-5 GcsXo')
                extract_data(properties, state)


def get_status(url):
# Iterating until page accepts the request
    for _ in range(40):
        html = requests.get(url, headers=headers)
        print(html.status_code)
        # Status code 200 means request succeeded, otherwise, keep trying it
        if html.status_code == 200:
            return html
    
    return False


def extract_data(properties, state):
    # Iterating over them to get their specific information
    for property in properties:  # Iterate through each property in the list
        # Extract the price and currency
        price = property.find('div', class_='sc-12dh9kl-3 dBiZcY').text.strip()
        currency = 'MX' if 'MN' in price else 'USD'  # Determine currency based on prefix
        price = int(price.removeprefix('MN ').replace(',', '').removeprefix('USD ').lower().replace('consultar precio', '0'))  # Clean and convert price to integer

        # Extract the maintenance fee
        value = property.find('div', class_='sc-12dh9kl-1 chzHQe')
        maintenance = int(value.text.strip().removeprefix('MN ').removesuffix(' Mantenimiento').replace(',', '').removeprefix('USD ')) if value else 'NULL'  # Clean and convert maintenance fee to integer, or set to 'NULL' if not found

        # Extract the neighborhood
        neighborhood = property.find('div', class_='sc-ge2uzh-1 gFoERH').div.text.strip().replace('\'', '\\\'').replace('"', '\\"')  # Escape single and double quotes
        neighborhood = 'NULL' if neighborhood == '' else neighborhood  # Set to 'NULL' if empty

        # Extract the location
        location = property.find('div', class_='sc-ge2uzh-1 gFoERH').h2.text.strip()
        location = 'NULL' if location == '' else location  # Set to 'NULL' if empty

        # Extract the description
        try:
            description = property.find('h3', class_='sc-i1odl-11 dnPeFf').text.strip().replace('\'', '\\\'').replace('"', '\\"')  # Escape single and double quotes
        except (AttributeError, TypeError) as e:
            description = 'NULL'  # Set to 'NULL' if not found

        # Extract the amenities
        try:
            amenities = ' '.join(span.get_text().replace('.', '') + ',' for span in property.find('h3', attrs={'data-qa': 'POSTING_CARD_FEATURES'})).removesuffix(',')  # Join amenities into a string
        except TypeError:
            amenities = 'NULL'  # Set to 'NULL' if not found

        # Parse the amenities string and extract specific information
        meters, rooms, bathroom, parking_spaces = parse_property_info(amenities)

        # Construct the SQL file path
        file_open = f'../db/{state["filename"]}.sql'

        # Write the property information to the SQL file
        with open(file_open, 'a') as file:
            file.write(f'INSERT INTO inm24 (price, maintenance, currency, property_state, neighborhood, property_address, meters, rooms, bathrooms, parking_spaces, property_description) values ({price}, {maintenance}, \'{currency}\', \'{state["name"]}\', \'{neighborhood}\', \'{location}\', {meters}, {rooms}, {bathroom}, {parking_spaces}, \'{description}\');\\n')


# this are characters followed into a specific bunch
def parse_property_info(amenities):
    # Initialize variables to store the extracted values
    meters, rooms, bathrooms, parking_spaces = '', '', '', ''
    
    # Split the amenities string into a list of individual amenities
    cases = amenities.split(',')
    
    # Iterate through each individual amenity
    for case in cases:
        # Check if the amenity contains 'm²' and not ' a ' (space + 'a' + space)
        if 'm²' in case and ' a ' not in case:
            # Extract the numeric value before 'm² tot' and convert it to an integer
            meters = int(case.replace(' m² tot', '').strip())
        
        # Check if the amenity contains 'rec' and not ' a '
        elif 'rec' in case and ' a ' not in case:
            # Extract the numeric value after 'rec' and convert it to an integer
            rooms = int(case.replace('rec', '').strip())
        
        # Check if the amenity contains 'baño' and not ' a '
        elif 'baño' in case and ' a ' not in case:
            # Extract the numeric value after 'baños' or 'baño' and convert it to an integer
            bathrooms = int(case.replace('baños', '').replace('baño', '').strip())
        
        # Check if the amenity contains 'esta' and not ' a '
        elif 'esta' in case and ' a ' not in case:
            # Extract the numeric value after 'estac' and convert it to an integer
            parking_spaces = int(case.replace('estac', '').strip())
    
    # Return a list with the extracted values or 'NULL' if no value was found
    return [meters or 'NULL', rooms or 'NULL', bathrooms or 'NULL', parking_spaces or 'NULL']

if __name__ == '__main__':
    main()