from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64
import time
import requests
from time import sleep

# Завантаження твого приватного ключа
private_key = Ed25519PrivateKey.from_private_bytes(base64.b64decode("LuZ7sDM/IKLnDSuBoUwnE2/COQTtZ84w0IhsCfRX0jI="))

# Генерація заголовків для запиту
def generate_headers(body_str):
    timestamp = int(time.time() * 1000)
    window = 5000

    # Створення підпису, включаючи тіло запиту
    sign_string = f"{body_str}&timestamp={timestamp}&window={window}"
    signature = private_key.sign(sign_string.encode())

    # Повернення заголовків
    return {
        "X-API-KEY": "Nh3cIkvbOKkDcUGGt0pcbdhEHf1gzfAR+UTF+dFN24s=",
        "X-SIGNATURE": base64.b64encode(signature).decode(),
        "X-TIMESTAMP": str(timestamp),
        "X-WINDOW": str(window),
    }


def make_buy_request():
    body = {
        "orderType": "Limit",
        "price": "2",
        "quantity": 20,
        "side": "Bid",
        "symbol": "JUP_USDC"
    }
    body_str = "instruction=orderExecute&" + "&".join(f"{k}={v}" for k, v in body.items())
    #print (body_str)
    headers = generate_headers(body_str)

    #print (headers)
    
    response = requests.post("https://api.backpack.exchange/api/v1/order", headers=headers, json=body)
    
    try:
        return response.json()
    except ValueError:
        print("Статус код:", response.status_code)
        print("Відповідь сервера:", response.text)
        return None

def make_sell_request():
    body = {
        "orderType": "Limit",
        "price": "1",
        "quantity": 19.97,
        "side": "Ask",
        "symbol": "JUP_USDC"
    }
    body_str = "instruction=orderExecute&" + "&".join(f"{k}={v}" for k, v in body.items())
    #print (body_str)
    headers = generate_headers(body_str)

    #print (headers)
    
    response = requests.post("https://api.backpack.exchange/api/v1/order", headers=headers, json=body)
    
    try:
        return response.json()
    except ValueError:
        print("Статус код:", response.status_code)
        print("Відповідь сервера:", response.text)
        return None

# Виведення відповіді

print("Початок роботи")

while True:
    response_data=make_buy_request()

    quantity=response_data.get('quantity')
    symbol=response_data.get('symbol')
    status=response_data.get('status')

    print("Bought "+quantity+" "+symbol+" "+status)

    sleep(1)

    

    make_sell_request()
    print("Sold "+ quantity+" "+symbol+" "+status)

    sleep(4)



