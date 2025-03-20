import random
from typing import Optional, List

from ..Client.Client import client 
from ..API.api import KEMONO_BASE_URL

class KemonoParty:
    @staticmethod
    async def fetch_posts(tag: Optional[str] = None, limit: int = 100) -> List[dict]:
        """
        Fetch posts from Kemono Party API based on a tag.

        Each post's 'file' and 'attachments' fields will have a new key 'full_url'
        containing the complete URL, constructed by prefixing the KEMONO_BASE_URL.
        """
        params = {"limit": limit}
        if tag:
            params["tag"] = tag.replace(" ", "_")

        url = f"{KEMONO_BASE_URL}/api/v1/posts"
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            posts = data.get("posts", [])
            
            for post in posts:
                if "file" in post and isinstance(post["file"], dict) and "path" in post["file"]:
                    post["file"]["full_url"] = f"{KEMONO_BASE_URL}{post['file']['path']}"
                
                if "attachments" in post and isinstance(post["attachments"], list):
                    for attachment in post["attachments"]:
                        if "path" in attachment:
                            attachment["full_url"] = f"{KEMONO_BASE_URL}{attachment['path']}"
            return posts
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []

    @staticmethod
    def is_valid_post(post: dict) -> bool:
        """
        Check if a post has a valid preview file and at least one valid attachment.
        """
        if "file" not in post or not isinstance(post["file"], dict) or not post["file"].get("path"):
            return False
        if "attachments" not in post or not isinstance(post["attachments"], list) or len(post["attachments"]) == 0:
            return False
        if not any(attachment.get("path") for attachment in post["attachments"]):
            return False
        return True

    @staticmethod
    async def fetch_nsfw_images(tag: Optional[str] = None) -> Optional[dict]:
        """
        Fetch a random NSFW image from Kemono Party by filtering valid posts.
        """
        posts = await KemonoParty.fetch_posts(tag=tag, limit=100)
        valid_posts = [post for post in posts if KemonoParty.is_valid_post(post)]
        return random.choice(valid_posts) if valid_posts else None
