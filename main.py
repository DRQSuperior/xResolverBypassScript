import random
import urllib.parse
import urllib.request
import socket
from bs4 import BeautifulSoup

with open('proxies.txt', 'r') as file:
    proxies = [line.strip() for line in file.readlines()]

gamertag = input("Enter the gamertag: ")

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'xresolver.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Cookie': 'User=admin; showAd=false;'
}

data = {
    'xboxUsername': gamertag.replace(' ', '+')
}

encoded_data = urllib.parse.urlencode(data).encode('utf-8')

while proxies:
    proxy = random.choice(proxies)

    proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener = urllib.request.build_opener(proxy_handler)
    request = urllib.request.Request('https://xresolver.com/ajax/tool.php', data=encoded_data, headers=headers)

    try:
        response = opener.open(request, timeout=5)
        soup = BeautifulSoup(response.read(), 'html.parser')

        if 'You can only resolve 1 user every 30 minutes.' in soup.text:
            print(f'Proxy {proxy} is on cooldown. Retrying with a new proxy...')
            proxies.remove(proxy)
            continue

        try:
            info = {
                'Gamertag': gamertag,
                'IP Address': soup.find(string='IP Address').find_next('td').get_text(strip=True),
                'Internet Service Provider': soup.find(string='Internet Service Provider').find_next('td').get_text(strip=True),
                'Latitude': soup.find(string='Latitude').find_next('td').get_text(strip=True),
                'Longitude': soup.find(string='Longitude').find_next('td').get_text(strip=True),
                'Postal Code': soup.find(string='Postal Code').find_next('td').get_text(strip=True),
                'City': soup.find(string='City').find_next('td').get_text(strip=True),
                'Country': soup.find(string='Country').find_next('td').get_text(strip=True),
                'Continent': soup.find(string='Continent').find_next('td').get_text(strip=True),
                'Region': soup.find(string='Region').find_next('td').get_text(strip=True),
                'District': soup.find(string='District').find_next('td').get_text(strip=True),
                'Timezone': soup.find(string='Timezone').find_next('td').get_text(strip=True),
                'Connection Type': soup.find(string='Connection Type').find_next('td').get_text(strip=True),
                'Currency': soup.find(string='Currency').find_next('td').get_text(strip=True)
            }
            print(info)
            break
        except AttributeError:
            print('No information found for this gamertag.')
            break
    except (urllib.error.URLError, socket.timeout):
        print(f'Request timed out with proxy: {proxy}. Retrying')
