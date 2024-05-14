from components.normalization import parse_property_info
from components.checkout import check_data_exists
import psycopg2

def extraction(properties, state):
    # Iterating over them to get their specific information
    for property in properties:  # Iterate through each property in the list
        # Extract the price and currency
        price = property.find(
            'div', attrs={'data-qa': 'POSTING_CARD_PRICE'}).text.strip()
        # Determine currency based on prefix
        currency = 'MX' if 'MN' in price else 'USD'
        price = int(price.removeprefix('MN ').replace(',', '').removeprefix('USD ').lower(
            # Clean and convert price to integer
        ).replace('consultar precio', 'NULL'))

        # Extract the maintenance fee
        value = property.find('div', attrs={'data-qa': 'expensas'})
        # Clean and convert maintenance fee to integer, or set to 'NULL' if not found
        maintenance = int(value.text.strip().removeprefix('MN ').removesuffix(
            ' Mantenimiento').replace(',', '').removeprefix('USD ')) if value else 'NULL'

        # Extract the neighborhood
        neighborhood = property.find('div', attrs={'data-qa': 'POSTING_CARD_LOCATION'}).div.text.strip(
            # Escape single and double quotes
        ).replace('\'', '\\\'').replace('"', '\\"')
        neighborhood = 'NULL' if neighborhood == '' else neighborhood  # Set to 'NULL' if empty

        # Extract the location
        location = property.find(
            'div', class_='LocationAddress-sc-ge2uzh-0 iylBOA postingAddress').h2.text.strip()
        location = 'NULL' if location == '' else location  # Set to 'NULL' if empty
        # Extract the description
        try:
            description = property.find('h3', attrs={'data-qa': 'POSTING_CARD_DESCRIPTION'}).text.strip(
                # Escape single and double quotes
            ).replace('\'', '\\\'').replace('"', '\\"')
        except (AttributeError, TypeError) as e:
            description = 'NULL'  # Set to 'NULL' if not found

        # Extract the amenities
        try:
            amenities = ' '.join(span.get_text().replace('.', '') + ',' for span in property.find(
                # Join amenities into a string
                'h3', attrs={'data-qa': 'POSTING_CARD_FEATURES'})).removesuffix(',')
        except TypeError:
            amenities = 'NULL'  # Set to 'NULL' if not found

        # Parse the amenities string and extract specific information
        meters, rooms, bathroom, parking_spaces = parse_property_info(
            amenities)

        # Establish connection to the database
        connection = psycopg2.connect(database='real_state',
                                    host='127.0.0.1',
                                    user='user',
                                    port='5432')

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        
        value_found = check_data_exists(connection, cursor, price, maintenance, currency, state_name, neighborhood, location, meters, rooms, bathroom, parking_spaces, description)

        if value_found:
            current_insert = 'INSERT INTO inm24 (price, maintenance, currency, property_state, neighborhood, property_address, meters, rooms, bathrooms, parking_spaces, property_description) values (' + f'{price}, {maintenance}, \'{currency}\', \'{state['name']}\', {neighborhood}, {location}, {meters}, {rooms}, {bathroom}, {parking_spaces}, {description});'    
            # Write the property information to the SQL file
            with open(file_open, 'a') as file:
                # Construct the SQL file path
                file_open = f'/Users/Santiago/Documents/OwnBuilding/RealWarehouse/db/inm24/data/{
                state['filename']}.sql'
                file.write('INSERT INTO inm24 (price, maintenance, currency, property_state, neighborhood, property_address, meters, rooms, bathrooms, parking_spaces, property_description) values (' + 
                        f'{price}, {maintenance}, \'{currency}\', \'{state['name']}\', {neighborhood}, {location}, {meters}, {rooms}, {bathroom}, {parking_spaces}, {description});')
                
                file.write('\n')

        else:
            return
        