import psycopg2

def check_data_exists(connection, cursor, price, maintenance, currency, state_name, neighborhood, location, meters, rooms, bathroom, parking_spaces, description):
    try:
        # Construct the SELECT query
        select_query = """
            SELECT * FROM inm24 
            WHERE price = %s 
            AND maintenance = %s 
            AND currency = %s 
            AND property_state = %s 
            AND neighborhood = %s 
            AND property_address = %s 
            AND meters = %s 
            AND rooms = %s 
            AND bathrooms = %s 
            AND parking_spaces = %s 
            AND property_description = %s
        """
        
        # Execute the SELECT query with the provided data
        cursor.execute(select_query, (price, maintenance, currency, state_name, neighborhood, location, meters, rooms, bathroom, parking_spaces, description))
        
        # Fetch the results
        result = cursor.fetchone()
        
        # Check if data exists
        if result:
            print("Data already exists in the database.")
            return True
        else:
            print("Data does not exist in the database.")
            return False
    except psycopg2.Error as e:
        print("Error checking data existence:", e)
        return Falsez