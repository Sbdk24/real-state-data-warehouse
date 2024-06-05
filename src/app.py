from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

from scripts.mx_states import get_states
from scripts.status import get_status
from scripts.psql import get_psql_client
from scrapings.extraction import extraction
from data.injection import Postgres

"""
Headers are a useful piece of information extracted your own 
credentials for letting the page know you're a human. 

You can find them opening the browser console and typing navigator.userAgent
"""
load_dotenv()

HEADER = {
    'Accept': '*/*', 
    'User-Agent': os.getenv('HEADER'),
    "Accept-Language": os.getenv('ACCEPT_LANG'),
    "Referer": os.getenv('REFER'),
}

cursor, connection = get_psql_client(host='127.0.0.1', port=5432, user='user', database='real_state_mx')

def main():
    total_of_properties = 0
    states = get_states()
    for state in states:
        data_not_repeated = True
        i = 1
        first_row_attached = {}
        while data_not_repeated: 
            # Url for inm24 current web page
            url = f'https://www.inmuebles24.com/inmuebles-en-venta-en-{
                state['url_key']}-pagina-{i}.html'

            html = get_status(url, headers_list=HEADER, payload="")

            # Start using BeautifulSoup with lxml which is currently the best parser
            """
            A parser is an HTML analizer who allow us to process and manipulate 
            XML and HTML text very efficiently and high performance.
            """
            if html:
                # Strart scraping all the properties we have on this particular page
                # There're always 20 per page
                inm24 = BeautifulSoup(html.text, 'lxml')

                properties = inm24.find_all(
                    'div', class_='CardContainer-sc-1tt2vbg-5 fvuHxG')

                for j, property in enumerate(properties):
                    data = extraction(property, total_of_properties)

                    if j == 0:
                        if first_row_attached == data:
                            print(f'No more data found for {state['name']}')
                            data_not_repeated = False
                            break
                        first_row_attached = data
                    Postgres(connection, cursor, data, state)
                    total_of_properties += 1

            i += 1
                    


if __name__ == '__main__':
    main()
