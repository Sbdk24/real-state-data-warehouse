import requests

def get_status(url, headers): 
# Iterating until page accepts the request
    for _ in range(6):
        html = requests.get(url, headers)
        print(html.status_code)
        # Status code 200 means request succeeded, otherwise, keep trying it
        if html.status_code == 200:
            return html
    
    return False