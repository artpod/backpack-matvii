from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64
import time
import requests
from time import sleep
from random import randint

# Завантаження твого приватного ключа
private_key = Ed25519PrivateKey.from_private_bytes(base64.b64decode("Sm4B/XHjh4eGxqUdy2W+HObnQ4Zf7gBIqbUSqDYb/XA="))

# Генерація заголовків для запиту
def generate_headers(body_str):
    timestamp = int(time.time() * 1000)
    window = 5000

    # Створення підпису, включаючи тіло запиту
    sign_string = f"{body_str}&timestamp={timestamp}&window={window}"
    signature = private_key.sign(sign_string.encode())

    # Повернення заголовків
    return {
        "X-API-KEY": "CfqglbacQGVj5gXpUvAoTn0XpRDSMWUtXyq4RUnn0pY=",
        "X-SIGNATURE": base64.b64encode(signature).decode(),
        "X-TIMESTAMP": str(timestamp),
        "X-WINDOW": str(window),
    }


def make_buy_request(price, quantity, symbol):
    body = {
        "orderType": "Limit",
        "price": price,
        "quantity": quantity,
        "side": "Bid",
        "symbol": symbol
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

def make_sell_request(price, quantity, symbol):
    body = {
        "orderType": "Limit",
        "price": price,
        "quantity": quantity,
        "side": "Ask",
        "symbol": symbol
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
    buy_price = input("Введіть ціну для покупки: ")
    sell_price = input("Введіть ціну для продажу: ")
    quantity = input("Введіть кількість для покупки: ")
    symbol = input("Введіть символ для покупки: ")

    # Вказуємо кількість ітерацій
    iterations = int(input("Введіть кількість ітерацій: "))

    # Ініціалізуємо лічильник
    current_iteration = 0

    sum = 0.0

    # Виконуємо цикл while до тих пір, поки лічильник менший за кількість ітерацій
    while current_iteration < iterations:
        response_data = make_buy_request(buy_price, quantity, symbol)

        quantity=response_data.get('quantity')
        symbol=response_data.get('symbol')
        status=response_data.get('status')

        print("Bought "+quantity+" "+symbol+" "+status)

        spi = randint(2, 15)
        print(f"Спимо {spi} секунд...")
        sleep(spi)

    

        response_data = make_sell_request(sell_price, quantity, symbol)
        print("Sold "+ quantity+" "+symbol+" "+status)

        spi = randint(2, 15)
        print(f"Спимо {spi} секунд...")
        sleep(spi)

        print("Ітерація номер "+str(current_iteration))
        print(" ")

        current_iteration += 1
        sum += float(quantity)*2

    print ("Прокручено "+str(sum)+" "+str(symbol))

