import random
from typing import Optional

from waifu_python import *

class RandomWaifu:
    
    fetch_images = [
        Danbooru.fetch_images,
        Yandere.fetch_images,
        Rule34.fetch_images,
    ]
    
    fetch_sfw_images = [
        WaifuIm.fetch_sfw_images,
        WaifuPics.fetch_sfw_images,
        Safebooru.fetch_images,  
        NekosBest.fetch_sfw_images,
        NSFWBot.fetch_sfw_images,
        PicRe.fetch_sfw_images,
        Konachan.fetch_sfw_images,
        Zerochan.fetch_sfw_images,
    ]
    
    fetch_nsfw_images = [
        WaifuIm.fetch_nsfw_images,
        WaifuPics.fetch_nsfw_images,
        Konachan.fetch_nsfw_images,
        NSFWBot.fetch_nsfw_images,
        KemonoParty.fetch_nsfw_images,
    ]
    
    fetch_sfw_gif = [
        PurrBot.fetch_sfw_gif,
    ]
    
    fetch_nsfw_gif = [
        PurrBot.fetch_nsfw_gif,
    ]

    @staticmethod
    async def _call_Random_func(func) -> Optional[str]:
        try:
            result = await func()  
            if isinstance(result, list):
                return result[0] if result else None
            return result
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None

    @staticmethod
    async def get_random_image() -> Optional[str]:
        """Fetch a random image URL."""
        func = random.choice(RandomWaifu.fetch_images)
        return await RandomWaifu._call_Random_func(func)

    @staticmethod
    async def get_random_sfw_image() -> Optional[str]:
        """Fetch a random sfw image URL."""
        func = random.choice(RandomWaifu.fetch_sfw_images)
        return await RandomWaifu._call_Random_func(func)

    @staticmethod
    async def get_random_nsfw_image() -> Optional[str]:
        """Fetch a random NSFW image URL."""
        func = random.choice(RandomWaifu.fetch_nsfw_images)
        return await RandomWaifu._call_Random_func(func)

    @staticmethod
    async def get_random_sfw_gif() -> Optional[str]:
        """Fetch a random sfw GIF URL."""
        func = random.choice(RandomWaifu.fetch_sfw_gif)
        return await RandomWaifu._call_Random_func(func)

    @staticmethod
    async def get_random_nsfw_gif() -> Optional[str]:
        """Fetch a random NSFW GIF URL."""
        func = random.choice(RandomWaifu.fetch_nsfw_gif)
        return await RandomWaifu._call_Random_func(func)
