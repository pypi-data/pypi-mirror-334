import random
from typing import Optional, Dict, Any

from ..API.api import WAIFUPICS_BASE_URL
from ..Client.Client import client

class WaifuPics:
    @staticmethod
    async def get_tags() -> Optional[Dict[str, Any]]:
        """Fetches all available tags from the /endpoints API."""
        url = f"{WAIFUPICS_BASE_URL}/endpoints"
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching tags: {e}")
            return None

    @staticmethod
    async def fetch_sfw_images(tag: Optional[str] = None, type: str = "sfw") -> Optional[str]:
        """
        Fetches a random SFW image from waifu.pics based on the given tag and type.
        If no tag is provided, a random tag is chosen from the available SFW tags.
        """
        type = type.lower()
        tags = await WaifuPics.get_tags()
        if tags is None or type not in tags:
            return None
        
        tag = tag or (random.choice(tags[type]) if tags[type] else None)
        if not tag:
            return None

        url = f"{WAIFUPICS_BASE_URL}/{type}/{tag}"
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("url")
        except Exception as e:
            print(f"Error fetching SFW image: {e}")
            return None

    @staticmethod
    async def fetch_nsfw_images(tag: Optional[str] = None, type: str = "nsfw") -> Optional[str]:
        """
        Fetches a random NSFW image from waifu.pics based on the given tag and type.
        If no tag is provided, a random tag is chosen from the available NSFW tags.
        """
        type = type.lower()
        tags = await WaifuPics.get_tags()
        if tags is None or type not in tags:
            return None
        
        tag = tag or (random.choice(tags[type]) if tags[type] else None)
        if not tag:
            return None

        url = f"{WAIFUPICS_BASE_URL}/{type}/{tag}"
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("url")
        except Exception as e:
            print(f"Error fetching NSFW image: {e}")
            return None
