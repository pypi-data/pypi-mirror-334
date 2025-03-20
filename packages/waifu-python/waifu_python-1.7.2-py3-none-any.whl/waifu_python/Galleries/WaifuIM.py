import random
from typing import Optional, Dict, Any

from ..API.api import WAIFUIM_BASE_URL
from ..Client.Client import client

class WaifuIm:
    @staticmethod
    async def fetch_image(tag: Optional[str] = None) -> Optional[str]:
        """
        Fetch an image from waifu.im API and return the direct image URL.
        If a tag is provided, it is included in the request parameters with spaces replaced by hyphens.
        """
        params = {}
        if tag:
            tag = tag.replace(" ", "-")  
            params["included_tags"] = tag
        
        url = f"{WAIFUIM_BASE_URL}search"
        
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            images = data.get("images", [])
            if images:
                return images[0].get("url")
        raise Exception(f"Failed to fetch image: {response.text}")

    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """
        Fetch available tags from waifu.im API.
        """
        url = f"{WAIFUIM_BASE_URL}tags"
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to fetch tags: {response.text}")

    @staticmethod
    async def fetch_sfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch an SFW image from waifu.im API.
        If no tag is provided, a random tag is chosen from the 'versatile' category.
        """
        tags = await WaifuIm.get_tags()
        if "versatile" not in tags:
            return None

        tag = tag.replace(" ", "-") if tag else random.choice(tags["versatile"])
        return await WaifuIm.fetch_image(tag)

    @staticmethod
    async def fetch_nsfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch an NSFW image from waifu.im API.
        If no tag is provided, a random tag is chosen from the 'nsfw' category.
        """
        tags = await WaifuIm.get_tags()
        if "nsfw" not in tags:
            return None

        tag = tag.replace(" ", "-") if tag else random.choice(tags["nsfw"])
        return await WaifuIm.fetch_image(tag)
