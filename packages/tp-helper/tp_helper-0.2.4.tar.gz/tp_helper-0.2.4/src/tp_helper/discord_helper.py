import logging
import aiohttp
from typing import Optional


class DiscordHelper:
    RED = 16711680
    GREEN = 5025616
    YELLOW = 16776960

    def __init__(self, url: str):
        self.url: str = url
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.color: Optional[int] = None
        self.notify_everyone: bool = False
        self.proxy: Optional[str] = None  # Прокси-сервер (по умолчанию отключен)

    def reset(self) -> "DiscordHelper":
        """Сбрасывает все параметры сообщения к значениям по умолчанию."""
        self.title = None
        self.description = None
        self.color = None
        self.notify_everyone = False
        return self

    def set_proxy(self, proxy_url: str) -> "DiscordHelper":
        """
        Устанавливает прокси-сервер (HTTP, HTTPS, SOCKS5).

        # HTTP-прокси (обычный)
        discord.set_proxy("http://1.1.1.1:1080")

        # HTTPS-прокси
        discord.set_proxy("https://user:password@proxy.example.com:8080")

        # SOCKS5-прокси (например, через Tor)
        discord.set_proxy("socks5h://127.0.0.1:9050")
        """
        self.proxy = proxy_url
        return self

    def set_title(self, title: str) -> "DiscordHelper":
        """Устанавливает заголовок сообщения."""
        self.title = title
        return self

    def set_description(self, description: str) -> "DiscordHelper":
        """Устанавливает описание сообщения."""
        self.description = description
        return self

    def set_color(self, color: int) -> "DiscordHelper":
        """Устанавливает цвет сообщения (в формате int)."""
        self.color = color
        return self

    def set_color_red(self) -> "DiscordHelper":
        """Устанавливает цвет сообщения на красный (ошибка)."""
        return self.set_color(self.RED)

    def set_color_green(self) -> "DiscordHelper":
        """Устанавливает цвет сообщения на зеленый (успех, информация)."""
        return self.set_color(self.GREEN)

    def set_color_yellow(self) -> "DiscordHelper":
        """Устанавливает цвет сообщения на желтый (предупреждение)."""
        return self.set_color(self.YELLOW)

    def set_notify_everyone(self, notify: bool) -> "DiscordHelper":
        """Определяет, следует ли упоминать @everyone в сообщении."""
        self.notify_everyone = notify
        return self

    async def send_with_level(
        self, level: str, message: str = None, desc: Optional[str] = None
    ):
        """Отправляет сообщение с заданным уровнем (Error, Warning, Info)."""
        if self.title is None:
            self.set_title(f"[{level}]")
        if desc:
            self.set_description(desc)
        self.set_notify_everyone(level == "Error")  # Уведомлять всех только при ошибке
        await self.send(message)

    async def send_error(self, message: str = None, desc: Optional[str] = None):
        """Отправляет сообщение об ошибке."""
        self.set_color_red()
        await self.send_with_level("Error", message, desc)

    async def send_warning(self, message: str = None, desc: Optional[str] = None):
        """Отправляет предупреждающее сообщение."""
        self.set_color_yellow()
        await self.send_with_level("Warning", message, desc)

    async def send_info(self, message: str = None, desc: Optional[str] = None):
        """Отправляет информационное сообщение."""
        self.set_color_green()
        await self.send_with_level("Info", message, desc)

    async def send(self, message: Optional[str] = None):
        """Отправляет сообщение с текущими параметрами."""
        if not message:
            message = ""
        await self._send_message(message)

    async def _send_message(self, message: str):
        """Отправляет сообщение в Discord через Webhook с использованием прокси (если задано)."""
        payload = {
            "content": f"{'@everyone ' if self.notify_everyone else ''}{message}",
            "tts": False,
            "username": "Система уведомлений",
            "embeds": [
                {
                    "title": self.title,
                    "description": self.description,
                    "color": self.color,
                }
            ],
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url, json=payload, proxy=self.proxy
                ) as response:
                    if response.status != 204:
                        logging.warning(
                            f"Ошибка отправки в Discord: {response.status} - {await response.text()}"
                        )
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения в Discord: {e}")

        self.reset()
