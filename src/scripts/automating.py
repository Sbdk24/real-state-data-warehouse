import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)' +
           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

states = [
    {'url_key': 'ciudad-de-mexico', 'filename': 'cdmx', 'name': 'ciudad de mexico'},
    {'url_key': 'edo.-de-mexico', 'filename': 'est_mx', 'name': 'estado de mexico'},
    {'url_key': 'queretaro-provincia', 'filename': 'queretaro', 'name': 'queretaro'},
    {'url_key': 'morelos-provincia', 'filename': 'morelos', 'name': 'morelos'},
    {'url_key': 'nuevo-leon', 'filename': 'nuevo_leon', 'name': 'nuevo leon'},
    {'url_key': 'yucatan', 'filename': 'yucatan', 'name': 'yucatan'},
    {'url_key': 'quintana-roo', 'filename': 'quintana_roo', 'name': 'quintana roo'},
    {'url_key': 'jalisco', 'filename': 'jalisco', 'name': 'jalisco'},
    {'url_key': 'veracruz-provincia', 'filename': 'veracruz', 'name': 'veracruz'},
    {'url_key': 'puebla-provincia', 'filename': 'puebla', 'name': 'puebla'},
    {'url_key': 'hidalgo-provicia', 'filename': 'hidalgo', 'name': 'hidalgo'},
    {'url_key': 'guerrero-provincia', 'filename': 'guerrero', 'name': 'guerrero'},
    {'url_key': 'san-luis-potosi-provincia', 'filename': 'sl_potosi', 'name': 'san luis potosi'},
    {'url_key': 'coahuila', 'filename': 'coahuila', 'name': 'coahuila'},
    {'url_key': 'durango-provincia', 'filename': 'durango', 'name': 'durango'},
    {'url_key': 'guanajuato-provincia', 'filename': 'guanajuato', 'name': 'guanajuato'},
    {'url_key': 'chiapas', 'filename': 'chiapas', 'name': 'chiapas'},
    {'url_key': 'chihuahua-provincia', 'filename': 'chihuahua', 'name': 'chihuahua'},
    {'url_key': 'tamaulipas', 'filename': 'tamaulipas', 'name': 'tamaulipas'},
    {'url_key': 'baja-california-norte', 'filename': 'bc_norte', 'name': 'baja california norte'}
]


# def check_list(state):
#     print(f'https://www.inmuebles24.com/inmuebles-en-venta-en-{state['url_key']}-pagina-.html')
#     print(f'../db/{state['filename']}.sql')
#     print(f'{state['name']}')

def main():
    for state in states:
        url = f'https://www.inmuebles24.com/inmuebles-en-venta-en-{state['url_key']}-pagina-.html'
        html = get_status(url)
        print(state['name']) if not html else print('200')


        

def get_status(url):
# Iterating until page accepts the request
    for _ in range(20):
        html = requests.get(url, headers=headers)
        # Status code 200 means request succeeded, otherwise, keep trying it
        print(html.status_code)
        if html.status_code == 200:
            return html
        
    return False



main()