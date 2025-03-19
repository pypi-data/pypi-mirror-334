from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "MCP4PY Server"
    admin_email: str
    items_per_user: int = 50
    
    class ConfigDict:
        from_attributes = True

settings = Settings(admin_email="<EMAIL>", items_per_user=1)