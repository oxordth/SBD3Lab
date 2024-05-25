import requests
import random
import string
import time
import datetime
import concurrent.futures

url = "http://localhost:8000/log"

event_types = ["login", "logout", "purchase"]
parameters_list = ["Login Successful", "Login Failed", "Purchase Successful", "Purchase Failed"]

def send_request():
    log_data = {
        "id": random.randint(1, 100000),
        "event_type": random.choice(event_types),
        "user_id": random.randint(1, 1000),
        "parameters": random.choice(parameters_list),
        "created_at": str(datetime.datetime.now())
    }
    try:
        response = requests.post(url, json=log_data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

while True:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Запускать несколько потоков для отправки запросов
        futures = [executor.submit(send_request) for _ in range(random.randint(1, 10))]  # Рандомное количество запросов
        for future in concurrent.futures.as_completed(futures):
            future.result()
    time.sleep(1)
