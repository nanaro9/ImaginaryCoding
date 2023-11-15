import requests
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
bitcoinPriceUSD = response.json()['bpi']['USD']['rate_float']

quantity = float(input("Ievadiet vēlamo Bitcoin daudzumu: "))
totalPrice = bitcoinPriceUSD*quantity
msg = f'{quantity} Bitcoin izmaksās: ${totalPrice}'
print(msg)
