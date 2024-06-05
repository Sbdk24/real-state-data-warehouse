from bs4 import BeautifulSoup
from extraction import extraction
from injection import Postgres
from psql import Client


def main():
    client = Client(host='127.0.0.1', port=5432, user='user', database='real_state_mx')

    with open('src/scrapings/tiriquitiqui.html', 'r') as file:
        html = file.read()
        if html:
            # Strart scraping all the properties we have on this particular page
            # There're always 20 per page
            inm24 = BeautifulSoup(html, 'lxml')
            properties = inm24.find_all(
                'div', class_='CardContainer-sc-1tt2vbg-5 fvuHxG')
            
            for property in properties: # Iterate through each property in the list
                values = extraction(property, 1) #[extraction(this_property, state='ciudad de mexico') for this_property in properties]

                Postgres(connection=client.connection, cursor=client.cursor, data=values, state='quintana roo')


main()