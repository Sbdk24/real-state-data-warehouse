from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from components.mx_states import get_states
from gather.inm24.extraction import extraction
from components.status import get_status

"""
Headers are a useful piece of information extracted your own 
credentials for letting the page know you're a human. 

You can find them opening the browser console and typing navigator.userAgent
"""
load_dotenv()

headers = {'User-Agent': os.getenv('HEADER')}

states = get_states()


def main():
    for state in states:
        """This is completely wrong"""
        for i in range(1000):
            # Url for inm24 current web page
            url = f'https://www.inmuebles24.com/inmuebles-en-venta-en-{
                state['url_key']}-pagina-{i + 1}.html'
            print(url)
            html = get_status(url, headers=headers)

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
                print(properties)
                extraction(properties, state)


if __name__ == '__main__':
    main()
