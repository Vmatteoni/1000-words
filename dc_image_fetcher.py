import requests
import datetime
import os

PEXELS_API_KEY = "vJr9V79W3LrPI86EJT0CFkLMjzKWJGcDFiBC8rS5IsEoYmxD4fIRT0ZB"
HEADERS = {"Authorization": PEXELS_API_KEY}

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_dc_image():
    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=HEADERS,
        params={"query": "Washington DC street photography", "per_page": 1}
    )
    data = response.json()
    if not data['photos']:
        raise Exception("No images found.")

    photo = data['photos'][0]
    image_url = photo['src']['original']
    photographer = photo['photographer']
    image_data = requests.get(image_url).content

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(IMAGE_DIR, f"dc_photo_{date_str}.jpg")

    with open(file_path, 'wb') as f:
        f.write(image_data)

    with open(os.path.join(IMAGE_DIR, f"dc_photo_{date_str}_credit.txt"), 'w') as f:
        f.write(f"Photo by {photographer} on Pexels")

    print(f"Image saved to {file_path}")
    print(f"Photo by {photographer} on Pexels")

if __name__ == "__main__":
    get_dc_image()
