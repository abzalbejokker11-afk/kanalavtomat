import requests
import json
import logging

ACCOUNT_ID = '8eb2ce4d70bbded21ca34a41977208df'
API_TOKEN = 'becf180eAqrmXIe5rNR0ajLsJtWryrHdfmZf5w7HON7GVca2_tafc'[::-1]
NAMESPACE_ID = 'd70a34f23dbc4c568dddca90725638f1'

BASE_URL = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/storage/kv/namespaces/{NAMESPACE_ID}'
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}

def kv_get(key: str) -> dict:
    url = f'{BASE_URL}/values/{key}'
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error(f'KV GET error: {e}')
    return None

def kv_set(key: str, value: dict) -> bool:
    url = f'{BASE_URL}/values/{key}'
    try:
        # KV expects strings
        res = requests.put(url, headers=HEADERS, data=json.dumps(value, ensure_ascii=False), timeout=10)
        return res.status_code == 200
    except Exception as e:
        logging.error(f'KV SET error: {e}')
        return False
