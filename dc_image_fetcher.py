import requests
import datetime
import os
import random
import sys

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)
LATEST_IMAGE_LOG = os.path.join(IMAGE_DIR, "latest_image.txt")

def get_dc_image():
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    if not PEXELS_API_KEY:
        raise EnvironmentError("❌ PEXELS_API_KEY environment variable is not set. Please set it to proceed.")

    HEADERS = {"Authorization": PEXELS_API_KEY.strip()}

    queries = [
        "Washington DC street photography",
        "Washington DC urban",
        "Capitol Hill",
        "National Mall DC",
        "Georgetown DC"
    ]

    last_url = None
    if os.path.exists(LATEST_IMAGE_LOG):
        with open(LATEST_IMAGE_LOG, 'r') as f:
            last_url = f.read().strip()

    for attempt in range(5):
        query = random.choice(queries)
        page = random.randint(1, 30)

        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=HEADERS,
            params={"query": query, "per_page": 1, "page": page}
        )
        data = response.json()
        if not data['photos']:
            continue

        photo = data['photos'][0]
        image_url = photo['src']['original']

        if image_url == last_url:
            print("Duplicate image detected. Retrying...")
            continue

        photographer = photo['photographer']
        image_data = requests.get(image_url).content

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(IMAGE_DIR, f"dc_photo_{date_str}.jpg")

        with open(file_path, 'wb') as f:
            f.write(image_data)

        with open(os.path.join(IMAGE_DIR, f"dc_photo_{date_str}_credit.txt"), 'w') as f:
            f.write(f"Photo by {photographer} on Pexels")

        with open(LATEST_IMAGE_LOG, 'w') as f:
            f.write(image_url)

        print(f"Image saved to {file_path}")
        print(f"Photo by {photographer} on Pexels")
        print(f"Image URL: {image_url}")
        return

    raise Exception("Failed to fetch a new image after 5 attempts.")

if __name__ == "__main__":
    get_dc_image()
