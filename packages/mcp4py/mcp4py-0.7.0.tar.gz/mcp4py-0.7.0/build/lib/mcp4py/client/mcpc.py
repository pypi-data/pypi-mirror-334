import requests
import json

class MCP4PYClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers= {'accept': 'application/json'}

    def get_item(self):
        r = requests.get(f"{self.base_url}/items",headers=self.headers)
        return r.json()
    def post_item(self, item: dict):
        url = f"{self.base_url}/items"
        r = requests.post(url,data=json.dumps(item),headers=self.headers)
        return r.json()
