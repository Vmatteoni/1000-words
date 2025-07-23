import requests
import datetime
import os
import random

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)
LATEST_IMAGE_LOG = os.path.join(IMAGE_DIR, "latest_image.txt")

def get_dc_md_va_image():
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    if not PEXELS_API_KEY:
        raise EnvironmentError("❌ PEXELS_API_KEY environment variable is not set. Please set it to proceed.")

    HEADERS = {"Authorization": PEXELS_API_KEY.strip()}

    queries = [
        "Washington DC street photography",
        "Capitol Hill at sunset",
        "Georgetown DC waterfront",
        "National Mall cherry blossoms",
        "Washington DC jazz club",
        "Washington DC live music",
        "Washington DC art gallery",
        "Washington DC public art",
        "Smithsonian museums",
        "Washington DC cultural festival",
        "Baltimore Inner Harbor",
        "Chesapeake Bay Maryland",
        "Annapolis Maryland harbor",
        "Great Falls Maryland",
        "Baltimore jazz music",
        "Maryland bluegrass festival",
        "Maryland mural art",
        "Maryland art festival",
        "Artscape Baltimore",
        "Old Town Alexandria Virginia",
        "Shenandoah National Park sunrise",
        "Arlington VA skyline",
        "Blue Ridge Mountains Virginia",
        "Wolf Trap Virginia concert",
        "Virginia wine and music festival",
        "Virginia art walk",
        "Charlottesville art festival"
    ]

    last_url = None
    if os.path.exists(LATEST_IMAGE_LOG):
        with open(LATEST_IMAGE_LOG, 'r') as f:
            last_url = f.read().strip()

    for attempt in range(5):
        query = random.choice(queries)
        page = random.randint(1, 10)

        try:
            response = requests.get(
                "https://api.pexels.com/v1/search",
                headers=HEADERS,
                params={"query": query, "per_page": 1, "page": page},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"⚠️ Request failed: {e}")
            continue

        photos = data.get('photos', [])
        if not photos:
            continue

        photo = photos[0]
        image_url = photo['src'].get('original') or photo['src'].get('large2x')
        if not image_url:
            continue

        if image_url == last_url:
            print("Duplicate image detected. Retrying...")
            continue

        photographer = photo.get('photographer', 'Unknown')
        image_data = requests.get(image_url).content

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(IMAGE_DIR, f"dc_photo_{date_str}.jpg")
        credit_path = os.path.join(IMAGE_DIR, f"dc_photo_{date_str}_credit.txt")

        with open(file_path, 'wb') as f:
            f.write(image_data)

        with open(credit_path, 'w') as f:
            f.write(f"Photo by {photographer} on Pexels")

        with open(LATEST_IMAGE_LOG, 'w') as f:
            f.write(image_url)

        print(f"✅ Image saved: {file_path}")
        print(f"📸 Photo by {photographer}")
        print(f"🔗 {image_url}")
        return

    raise Exception("❌ Failed to fetch a new image after 5 attempts.")

if __name__ == "__main__":
    get_dc_md_va_image()
