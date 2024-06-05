import psycopg2

# Function to perform the operations
def insert_related_records(val1, val2, val3, val4):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        conn.autocommit = False  # Disable autocommit to manage transactions manually

        with conn.cursor() as cur:
            # Step 1: Insert into table1 and get the generated ID
            cur.execute("INSERT INTO table1 (col1, col2) VALUES (%s, %s) RETURNING id;", (val1, val2))
            table1_id = cur.fetchone()[0]

            # Step 2: Insert into table2 with the relation to table1 and get the generated ID
            cur.execute("INSERT INTO table2 (col1, col2, table1_id) VALUES (%s, %s, %s) RETURNING id;", (val3, val4, table1_id))
            table2_id = cur.fetchone()[0]

            # Step 3: Update table1 with the relation to table2
            cur.execute("UPDATE table1 SET table2_id = %s WHERE id = %s;", (table2_id, table1_id))

        # Commit the transaction
        conn.commit()

        print(f"Records inserted successfully: table1_id={table1_id}, table2_id={table2_id}")

    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection
        conn.close()

# Example usage
insert_related_records('value1', 'value2', 'value3', 'value4')