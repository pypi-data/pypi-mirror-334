# luziip.py
import requests

def fetch_ip_info(ip):
    url = f'http://ip-api.com/json/{ip}'  # HTTP kullanarak bağlantı kuruyoruz
    response = requests.get(url, verify=False)  # SSL doğrulaması kapalı
    data = response.json()

    if data['status'] == 'fail':
        return f"Error: {data['message']}"

    return data
