import os
import json
from .types import JsonVar
from .keys import key_list

def get_formated_environ_var(key: str) -> str:
    return (
        os.environ.get(key).
        replace("'",'"').
        replace("None", "null").
        replace("True","true").
        replace("False","false")
    ).replace("'",'"')

def get_env(key: str) -> JsonVar:
    json_var: JsonVar = json.loads(get_formated_environ_var(key))
    if isinstance(json_var, list):
        for item in json_var:
            if isinstance(item, str): item = json.dumps(item).replace('"', '')
    elif isinstance(json_var, dict):
        for key, val in json_var.items():
            if isinstance(val, str): json_var[key] = json.dumps(val).replace('"','')
    return json_var

def show_all() -> None:
    for key in key_list:
        val: JsonVar = get_env(key)
        print(f"key: {key}, val: {val}, type: {type(val)}")