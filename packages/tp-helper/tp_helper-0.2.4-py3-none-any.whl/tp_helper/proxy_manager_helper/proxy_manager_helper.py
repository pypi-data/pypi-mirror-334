import aiohttp

from .schemas.proxy_schema import ProxySchema


class ProxyManagerHelper:
    def __init__(self, proxy_manager_url: str):
        self.proxy_manager_url = proxy_manager_url

    async def get_one_proxy(self, queue: str) -> ProxySchema:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.proxy_manager_url + "/proxies", params={"queue": queue}
            ) as response:
                proxy_text = await response.text()
                return ProxySchema.model_validate_json(proxy_text)
