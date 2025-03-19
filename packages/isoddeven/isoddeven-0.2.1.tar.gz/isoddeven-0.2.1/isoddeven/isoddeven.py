import requests
import json

def is_odd(n: int) -> bool:
    response = requests.get(f"https://is-odd-api.mewtru.com/v1/numbers/{n}")
    json_data = json.loads(response.text)
    state = json_data["state"]
    if state == "odd":
        return True
    else:
        return False

def is_even(n: int) -> bool:
    response = requests.get(f"https://is-odd-api.mewtru.com/v1/numbers/{n}")
    json_data = json.loads(response.text)
    state = json_data["state"]
    if state == "even":
        return True
    else:
        return False

def state(n: int) -> str:
    response = requests.get(f"https://is-odd-api.mewtru.com/v1/numbers/{n}")
    json_data = json.loads(response.text)
    state = json_data["state"]
    return state
