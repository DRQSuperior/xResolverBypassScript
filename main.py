import random
import requests

with open('proxies.txt', 'r') as file:
    proxies = [line.strip() for line in file.readlines()]

proxy = random.choice(proxies)

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

response = requests.post('https://xresolver.com/ajax/tool.php', headers=headers, data=data, proxies={'http': proxy, 'https': proxy})

print(response.text)
