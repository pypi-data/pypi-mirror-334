import random
from typing import Optional, Dict, Any

from ..API.api import PURRBOT_BASE_URL
from ..Client.Client import client

class PurrBot:
    purrbot_nsfw_tags = [
        "anal", "blowjob", "cum", "fuck", "pussylick", "solo", "solo_male",
        "threesome_fff", "threesome_ffm", "threesome_mmf", "yaoi", "yuri", "neko"
    ]
    
    purrbot_tags = ["eevee", "holo", "icon", "kitsune", "neko", "okami", "senko", "shiro"]

    purrbot_reactions = [
        "angry", "bite", "blush", "comfy", "cry", "cuddle", "dance", "fluff",
        "hug", "kiss", "lay", "lick", "pat", "neko", "poke", "pout", "slap", 
        "smile", "tail", "tickle", "eevee"
    ]

    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """Return a dictionary of SFW and NSFW tags."""
        return {
            "sfw": PurrBot.purrbot_tags + PurrBot.purrbot_reactions,
            "nsfw": PurrBot.purrbot_nsfw_tags
        }

    @staticmethod
    async def fetch_sfw_gif(reaction: Optional[str] = None, tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch a SFW gif from purrbot.site based on a reaction and tag.
        Automatically converts spaces in the tag to underscores.
        """
        if not reaction:
            reaction = random.choice(PurrBot.purrbot_reactions)
        
        if reaction not in PurrBot.purrbot_reactions:
            return {"error": "Invalid reaction"}
        
        if not tag:
            tag = random.choice(PurrBot.purrbot_reactions)
        else:
            tag = tag.replace(" ", "_")
        
        if tag not in (PurrBot.purrbot_reactions + PurrBot.purrbot_tags):
            return {"error": "Invalid tag"}
    
        url = f"{PURRBOT_BASE_URL}/img/sfw/{reaction}/gif"
        params = {"tag": tag}
    
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("link") or {"error": "No link found"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def fetch_nsfw_gif(tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch an NSFW gif from purrbot.site based on a tag.
        Automatically converts spaces in the tag to underscores.
        """
        if not tag:
            tag = random.choice(PurrBot.purrbot_nsfw_tags)
        else:
            tag = tag.replace(" ", "_")
        
        if tag not in PurrBot.purrbot_nsfw_tags:
            return {"error": "Invalid NSFW tag"}

        url = f"{PURRBOT_BASE_URL}/img/nsfw/{tag}/gif"
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("link") or {"error": "No link found"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def fetch_sfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch a SFW image from purrbot.site based on a tag.
        Automatically converts spaces in the tag to underscores.
        """
        if not tag:
            tag = random.choice(PurrBot.purrbot_tags)
        else:
            tag = tag.replace(" ", "_")
        
        if tag not in PurrBot.purrbot_tags:
            return {"error": "Invalid tag"}
        
        url = f"{PURRBOT_BASE_URL}/img/sfw/{tag}/img"
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("link") or {"error": "No link found"}
        except Exception as e:
            return {"error": str(e)}
