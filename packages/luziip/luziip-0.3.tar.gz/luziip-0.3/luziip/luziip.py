# luziip/luziip.py
import requests

def fetch_ip_info(ip):
    url = f'https://ip-api.com/json/{ip}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'fail':
        return f"Error: {data['message']}"

    return data
