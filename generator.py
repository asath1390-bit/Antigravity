import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import uuid
import config

class ContentGenerator:
    def generate(self):
        raise NotImplementedError("Subclasses must implement generate()")

class QuoteGenerator(ContentGenerator):
    def __init__(self):
        self.quote_api_url = "https://dummyjson.com/quotes/random"
        self.image_api_url = "https://picsum.photos/1080/1080" # Random square image

    def fetch_quote(self):
        try:
            response = requests.get(self.quote_api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return f"\"{data['quote']}\"", f"- {data['author']}"
        except Exception as e:
            print(f"Error fetching quote: {e}")
            return "\"The only way to do great work is to love what you do.\"", "- Steve Jobs"

    def fetch_background_image(self, save_path):
        try:
            response = requests.get(self.image_api_url, stream=True, timeout=10)
            response.raise_for_status()
            with open(save_path, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            return True
        except Exception as e:
            print(f"Error fetching image: {e}")
            # Create a simple colored background if fetch fails
            img = Image.new('RGB', (1080, 1080), color = (73, 109, 137))
            img.save(save_path)
            return True

    def process_image(self, image_path, quote, author):
        # Open image
        img = Image.open(image_path).convert("RGBA")
        
        # Add dark overlay for readability
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 128))
        img = Image.alpha_composite(img, overlay)
        img = img.convert("RGB") # Convert back to RGB for saving as JPG

        draw = ImageDraw.Draw(img)
        
        # Load font
        font_size = 60
        try:
            font = ImageFont.truetype(config.DEFAULT_FONT, font_size)
            author_font = ImageFont.truetype(config.DEFAULT_FONT, int(font_size * 0.7))
        except OSError:
            font = ImageFont.load_default()
            author_font = ImageFont.load_default()

        # Wrap text
        image_width, image_height = img.size
        char_width = font_size * 0.5 # Approximate
        max_chars = int(image_width * 0.8 / char_width)
        
        lines = textwrap.wrap(quote, width=30) # Hardcoded wrap width is safer than calculating
        
        # Calculate total text height to center it
        # ascent, descent = font.getmetrics()
        # line_height = ascent + descent
        line_height = font_size * 1.5
        total_text_height = len(lines) * line_height + line_height # +1 for author
        
        current_y = (image_height - total_text_height) / 2
        
        # Draw Quote
        for line in lines:
            # text_width = draw.textlength(line, font=font) # specific to newer Pillow
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (image_width - text_width) / 2
            draw.text((x, current_y), line, font=font, fill="white")
            current_y += line_height
            
        # Draw Author
        current_y += 20 # Padding
        bbox = draw.textbbox((0, 0), author, font=author_font)
        text_width = bbox[2] - bbox[0]
        x = (image_width - text_width) / 2
        draw.text((x, current_y), author, font=author_font, fill="#DDDDDD")

        img.save(image_path)
        return image_path

    def generate(self):
        quote, author = self.fetch_quote()
        filename = f"post_{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join(config.OUTPUT_DIR, filename)
        
        if self.fetch_background_image(filepath):
            self.process_image(filepath, quote, author)
            print(f"Generated content: {filepath} | Quote: {quote}")
            return filepath, f"{quote} {author} #motivation #quote #dailyquotes"
        return None, None

if __name__ == "__main__":
    generator = QuoteGenerator()
    generator.generate()
