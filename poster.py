from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import config
import time

class InstagramPoster:
    def __init__(self):
        self.cl = Client()
        self.session_file = os.path.join(config.BASE_DIR, "session.json")

    def login(self):
        """
        Logins to Instagram. Tries to load session first.
        """
        if os.path.exists(self.session_file):
            print("Loading session from file...")
            self.cl.load_settings(self.session_file)
        
        try:
            self.cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)
            self.cl.dump_settings(self.session_file)
            print(f"Logged in as {config.INSTAGRAM_USERNAME}")
            return True
        except Exception as e:
            print(f"Failed to login: {e}")
            return False

    def upload_photo(self, image_path, caption):
        """
        Uploads a photo to Instagram
        """
        if not self.login():
            print("Cannot upload, login failed.")
            return False

        print(f"Uploading {image_path}...")
        try:
            media = self.cl.photo_upload(
                path=image_path,
                caption=caption
            )
            print(f"Photo uploaded! Media ID: {media.pk}")
            return True
        except Exception as e:
            print(f"Failed to upload photo: {e}")
            return False

if __name__ == "__main__":
    # Test login only
    if config.INSTAGRAM_USERNAME and config.INSTAGRAM_PASSWORD:
        poster = InstagramPoster()
        poster.login()
    else:
        print("Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env to test login.")
