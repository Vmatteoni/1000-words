# 1000 Words – Daily D.C. Photo Fetcher

Automatically downloads a daily public-domain or open-license photo of Washington, D.C. from Pexels and saves it to this repo, including photographer credit.

## How It Works

- Uses the Pexels API to search for urban/street photography in Washington, D.C.
- Saves the image and attribution daily into the `/images` folder.
- Scheduled via GitHub Actions to run once per day.

## Setup

1. Add a secret to your repo:
   - Name: `PEXELS_API_KEY`
   - Value: Your Pexels API key

2. Images will appear in `/images` daily with filenames like `dc_photo_YYYY-MM-DD.jpg`.

## License

Images sourced via Pexels API – free for personal and commercial use, with attribution.
