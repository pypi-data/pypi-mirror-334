import random
from typing import Optional

from ..API.api import NEKOS_BASE_URL
from ..Client.Client import client

class NekosBest:
    tags = []

    @staticmethod
    async def get_tags() -> list:
        """Fetches all available tags from the endpoints API."""
        url = f"{NEKOS_BASE_URL}/endpoints"
        response = await client.get(url)
        if response.status_code == 200:
            NekosBest.tags = list(response.json().keys())
        else:
            NekosBest.tags = []
        return NekosBest.tags

    @staticmethod
    async def fetch_sfw_images(tag: Optional[str] = None) -> Optional[str]:
        """
        Fetches a random image/GIF from nekos.best based on the given tag.
        """
        if not NekosBest.tags:
            await NekosBest.get_tags()
        
        tag = tag or random.choice(NekosBest.tags)
        url = f"{NEKOS_BASE_URL}/{tag}"
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            images = data.get("results", [])
            if images:
                return images[0].get("url")
        return None
