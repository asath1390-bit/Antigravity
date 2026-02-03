import schedule
import time
import config
from generator import QuoteGenerator
from poster import InstagramPoster
import os

def job():
    print("Starting scheduled job...")
    
    # 1. Generate Content
    gen = QuoteGenerator()
    image_path, caption = gen.generate()
    
    if image_path and caption:
        # 2. Post Content
        poster = InstagramPoster()
        # Only attempt to post if credentials are set, otherwise just log
        if config.INSTAGRAM_USERNAME and config.INSTAGRAM_PASSWORD:
            poster.upload_photo(image_path, caption)
        else:
            print(f"DRY RUN: Would post {image_path} with caption: {caption}")
            print("To enable posting, set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")
    else:
        print("Failed to generate content.")

def start_scheduler():
    # Schedule the job
    # For testing purposes, we can uncomment the next line to run every minute
    # schedule.every(1).minutes.do(job)
    
    # Actual schedule: Every day at 10:00 AM
    schedule.every().day.at("10:25").do(job)
    
    print("Scheduler started. Waiting for jobs...")
    
    # Run once immediately for demonstration if requested
    # job() 
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    job() # Run once immediately when script is executed manually
