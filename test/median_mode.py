import psycopg2

# List of states
states = [
    {'name': 'baja california norte'},
    {'name': 'chiapas'},
    {'name': 'chihuahua'},
    {'name': 'ciudad de mexico'},
    {'name': 'coahuila'},
    {'name': 'durango'},
    {'name': 'estado de mexico'},
    {'name': 'guanajuato'},
    {'name': 'guerrero'},
    {'name': 'hidalgo'},
    {'name': 'jalisco'},
    {'name': 'morelos'},
    {'name': 'nuevo leon'},
    {'name': 'puebla'},
    {'name': 'queretaro'},
    {'name': 'quintana roo'},
    {'name': 'san luis potosi'},
    {'name': 'tamaulipas'},
    {'name': 'yucatan'},
    {'name': 'veracruz'}
]

# Establish connection to the database
connection = psycopg2.connect(database='real_state',
                              host='127.0.0.1',
                              user='user',
                              port='5432')

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Iterate over each state
for state in states:
    # Execute query to find the median price for the current state
    cursor.execute(f"""
        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY price::numeric) AS mediana
        FROM inm24 WHERE property_state = '{state['name']}'; 
        """
    )
    # Print the result of the query
    print(cursor.fetchone())

# Iterate over each state
for state in states:
    # Execute query to find the mode price and its frequency for the current state
    cursor.execute(f"""
        SELECT DISTINCT price AS mode_price, COUNT(*) 
        OVER (PARTITION BY price::numeric) AS frequency 
        FROM inm24 WHERE property_state = '{state['name']}'
        ORDER BY frequency DESC LIMIT 1;
        """
    )
    # Print the result of the query
    print(cursor.fetchone())

# Close the database connection
connection.close()

