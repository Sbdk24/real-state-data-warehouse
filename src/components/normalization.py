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