from bs4 import BeautifulSoup
import requests

HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

def main():
    # Url for inm24 current web page
    url = 'https://century21mexico.com/propiedad/536096_casa-en-venta-en-santerra-hermosillo-sonora-mexico'

    print(url)
    html = get_status(url)

    # Strart scraping all the properties we have on this particular page
    inm24 = BeautifulSoup(html.text, 'lxml')
    print(inm24)
    # properties = inm24.find('h6', class_='text-muted fs-3 fw-bold')
    # print(properties)


def get_status(url): 
# Iterating until page accepts the request
    for _ in range(40):
        html = requests.get(url, headers=HEADER)
        print(html.status_code)
        # Status code 200 means request succeeded, otherwise, keep trying it
        if html.status_code == 200:
            return html
    
    return False

main()