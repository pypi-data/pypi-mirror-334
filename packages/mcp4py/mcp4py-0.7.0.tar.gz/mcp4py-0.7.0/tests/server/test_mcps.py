import uvicorn
from mcp4py.server.mcps import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
