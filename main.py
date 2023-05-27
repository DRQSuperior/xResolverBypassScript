import random
import urllib.parse
import urllib.request
import socket

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
        print(response.read().decode('utf-8'))
        break
    except (urllib.error.URLError, socket.timeout):
        print(f'Request timed out with proxy: {proxy}. Retrying with a new proxy...')
        proxies.remove(proxy)
else:
    print('No more proxies to try. Request failed.')
