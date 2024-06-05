import psycopg2
from src.scrapings.extraction import Extractor

class Postgres:
    def __init__(self, connection: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor, data: dict, state: str) -> None:
        self.connection = connection
        self.cursor = cursor
        #self.advertiser = advertiser Maybe later
        self.data, self.state = data, state

        self.data_insertion()

    def main_table_insertion(self, orchestrator):
        state_id = self.get_state_id()

        command = "INSERT INTO properties (price, maintenance, currency, location_p, address_p, meters, rooms, bathrooms, parking_spaces, state_id, advertiser_id) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s) RETURNING id;"
        values = (self.data["price"], self.data["maintenance"], self.data["currency"], self.data["location"], self.data["address"],
                self.data["meters"], self.data["rooms"], self.data["bathrooms"], self.data["parking_spaces"], state_id, 1)

        orchestrator.execute(command, values)

        return orchestrator.fetchone()[0]

    def single_table_insertion(self, orchestrator, property_id, table: str, column:str):
        command = f"INSERT INTO {table} (property_id, {column}) VALUES (%s, %s)"
        values = (property_id, self.data[column])

        orchestrator.execute(command, values)
        
        return orchestrator.fetchone()[0]
    
    def edit_row(self):
        pass

    def delete_row(self):
        pass

    
    def get_state_id(self) -> int:
        self.cursor.execute(f"SELECT id FROM states WHERE state_name = \'{self.state}\';")
        state_id = self.cursor.fetchone()[0] 

        return state_id 

    def data_insertion(self):
        description_id, link_id = 'NULL', 'NULL'
        try:
            with self.cursor as orchestrator:
                property_id = self.main_table_insertion(orchestrator)

                if Extractor.is_filled(self.data["link"]): 
                    description_id = self.single_table_insertion(orchestrator, property_id, table="links", column="link")

                if Extractor.is_filled(self.data["description_p"]): 
                    link_id = self.single_table_insertion(orchestrator, property_id, table="descriptions", column="description_p")

                if Extractor.is_filled(self.data["image_p"]): 
                    self.cursor.execute("INSERT INTO images (image_p) VALUES (%s)", (psycopg2.Binary(self.data["images"])))

                orchestrator.execute("UPDATE properties SET link_id = %s, description_id = %s WHERE id = %s;", (link_id, description_id, property_id))

            self.connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.connection.rollback()
            print(f"An error occurred: {e}")

        
            
