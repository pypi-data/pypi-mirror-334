from mcp4py.client.mcpc import MCP4PYClient


client = MCP4PYClient("http://127.0.0.1:8000")
item = client.post_item({
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
})
print(item)