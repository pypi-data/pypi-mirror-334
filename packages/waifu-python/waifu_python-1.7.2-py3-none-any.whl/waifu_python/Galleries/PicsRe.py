import random
from typing import Optional, List, Dict, Any

from ..API.api import PICRE_BASE_URL
from ..Client.Client import client

class PicRe:
    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """Fetch available tags from pic.re API."""
        url = f"{PICRE_BASE_URL}tags"
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching tags: {e}")
            return {}

    @staticmethod
    async def fetch_sfw_images(tags: Optional[List[str]] = None) -> Optional[str]:
        """
        Fetch a safe-for-work image URL from pic.re API based on tags.

        Automatically replaces spaces in each tag with underscores.
        """
        params = {}
        if tags:
            params["in"] = ",".join(tag.replace(" ", "_") for tag in tags)
        
        url = f"{PICRE_BASE_URL}image.json"
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("file_url")
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None
