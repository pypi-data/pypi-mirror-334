from pydantic import BaseModel


class ProxySchema(BaseModel):
    login: str
    password: str
    ip: str
    port: int
