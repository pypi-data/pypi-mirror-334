from mcp4py.server.api.prompts import Prompts
from mcp4py.server.api.resources import Resources
from mcp4py.server.api.tools import Tools
import uvicorn



class MCPS(Prompts,Resources,Tools):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, host: str = "0.0.0.0", port: int = 8000, **kwargs):
        uvicorn.run(self, host=host, port=port, **kwargs)

