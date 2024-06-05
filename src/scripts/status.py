import requests

def get_status(url, headers_list, payload): 
# Iterating until page accepts the request
    for _ in range(4):
        try:
            html = requests.request("GET", url, data=payload, headers=headers_list, timeout=2)
            print(html.status_code)
            # Status code 200 means request succeeded, otherwise, keep trying it
            if html.status_code == 200:
                return html
        except requests.exceptions.Timeout:
            print("The request timed out")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    
    return False