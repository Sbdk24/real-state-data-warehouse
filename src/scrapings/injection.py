import psycopg2
from extraction import Extractor

class Postgres:
    def __init__(self, connection: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor, data: dict, state: str) -> None:
        self.connection = connection
        self.cursor = cursor
        #self.advertiser = advertiser Maybe later
        self.data, self.state = data, state
        self.data_insertion()

    def main_table_insertion(self):
        state_id = self.get_state_id()

        command = "INSERT INTO properties (price, maintenance, currency, location_p, address_p, meters, rooms, bathrooms, parking_spaces, state_id, advertiser_id) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s) RETURNING id;"
        values = (self.data["price"], self.data["maintenance"], self.data["currency"], self.data["location_p"], self.data["address_p"],
                self.data["meters"], self.data["rooms"], self.data["bathrooms"], self.data["parking_spaces"], state_id, 1)

        self.cursor.execute(command, values)
        property_id = self.cursor.fetchone()[0]
        return property_id

    def single_table_insertion(self, property_id, table: str, column:str):
        command = f"INSERT INTO {table} (property_id, {column}) VALUES (%s, %s) RETURNING id;"
        values = (property_id, self.data[column])

        self.cursor.execute(command, values)
        
        return self.cursor.fetchone()[0]
    
    # def edit_row(self):
    #     pass

    # def delete_row(self):
    #     pass

    
    def get_state_id(self) -> int:
        self.cursor.execute("SELECT id FROM states WHERE state_name = %s;", (self.state,))
        state_id = self.cursor.fetchone()[0] 
        return state_id 
    

    def data_insertion(self):
        print("price", self.data["price"])
        print("maintenance", self.data["maintenance"])
        print("currency", self.data["currency"])
        print("location_p", self.data["location_p"])
        print("address_p", self.data["address_p"])
        print("meters", self.data["meters"])
        print("rooms", self.data["rooms"])
        print("bathrooms", self.data["bathrooms"])
        print("parking_spaces", self.data["parking_spaces"])
        print("link", self.data["link"])

        description_id, link_id = None, None
        try:
            property_id = self.main_table_insertion()


            if Extractor.is_filled(self.data["link"]): 
                link_id = self.single_table_insertion(property_id, table="links", column="link")

            if Extractor.is_filled(self.data["description_p"]): 
                description_id = self.single_table_insertion(property_id, table="descriptions", column="description_p")

            if Extractor.is_filled(self.data["image_p"]): 
                self.cursor.execute("INSERT INTO images (property_id, image_p) VALUES (%s, %s);", (property_id, psycopg2.Binary(self.data["image_p"])))

            print("property_id: ", property_id)
            print("description_id: ", description_id)
            print("link_id: ", link_id)
            print("\n\n\n")

            self.cursor.execute("UPDATE properties SET link_id = %s, description_id = %s WHERE id = %s;", (link_id, description_id, property_id))

            #self.connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.connection.rollback()
            print(f"An error occurred: {e}")

        
            
