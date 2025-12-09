import asyncio
import csv
import pandas as pd
from playwright.async_api import async_playwright
import re

# -----------------------------------------
# Global settings
# -----------------------------------------
RENT_BASE = "https://www.homegate.ch/louer/biens-immobiliers/npa-{ZIP}/liste-annonces"
OUTPUT_CSV = "rent_results.csv"
CONCURRENCY = 8  # Number of ZIP codes to process in parallel


# -----------------------------------------
# Helper: extract first number from messy text
# -----------------------------------------
def clean_number(text):
    if not text:
        return "N/A"
    text = text.replace("’", "").replace(" ", "")
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    return m.group(1) if m else "N/A"


# -----------------------------------------
# Scrape a single ZIP code
# -----------------------------------------
async def scrape_zip(zip_code, playwright):

    url = RENT_BASE.replace("{ZIP}", str(zip_code))
    print(f"\n🌍 Starting ZIP {zip_code} → {url}")

    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # Load page with retries
    success = False
    for attempt in range(3):
        try:
            await page.goto(url, timeout=60000)
            success = True
            break
        except:
            print(f"⚠ ZIP {zip_code}: goto failed ({attempt+1}/3), retrying...")
            await asyncio.sleep(1)

    if not success:
        print(f"❌ ZIP {zip_code}: failed to load page.")
        await browser.close()
        return []

    # Accept cookies if shown
    try:
        await page.click("#onetrust-accept-btn-handler", timeout=3000)
    except:
        pass

    # Check empty-page message
    if await page.locator("text=La pagina richiesta non può essere visualizzata").count() > 0:
        print(f"⚠ ZIP {zip_code}: empty page → skipping.")
        await browser.close()
        return []

    # Extra wait to ensure cards load
    await asyncio.sleep(2)

    # Wait for listings (or timeout)
    try:
        await page.wait_for_selector("div[data-test='result-list-item']", timeout=15000)
    except:
        print(f"⚠ ZIP {zip_code}: no listings found.")
        await browser.close()
        return []

    # Extract listing cards
    cards = page.locator("div[data-test='result-list-item']")
    count = await cards.count()
    print(f"📦 ZIP {zip_code}: found {count} listings")

    rows = []

    # Extract for each listing
    for i in range(count):
        card = cards.nth(i)

        # URL
        try:
            href = await card.locator("a.HgCardElevated_content_900d9").get_attribute("href")
            full_url = href if href.startswith("http") else "https://www.homegate.ch" + href
        except:
            full_url = "N/A"

        # Price
        try:
            price_raw = await card.locator("span[class*='price']").inner_text()
            price = clean_number(price_raw)
        except:
            price = "N/A"

        # Rooms
        try:
            rooms_raw = await card.locator("div[class*='ListingRoomsLivingSpace'] strong").nth(0).inner_text()
            rooms = clean_number(rooms_raw)
        except:
            rooms = "N/A"

        # Area m2
        try:
            area_raw = await card.locator("div[class*='ListingRoomsLivingSpace'] strong").nth(1).inner_text()
            area = clean_number(area_raw)
        except:
            area = "N/A"

        rows.append([zip_code, full_url, price, rooms, area])

    await browser.close()
    return rows


# -----------------------------------------
# Parallel executor (8 at a time)
# -----------------------------------------
async def run_all():
    df = pd.read_csv("data/zip_codes_selected.csv")
    zip_list = df["zip"].tolist()

    final_rows = []

    async with async_playwright() as pw:

        # Process ZIP codes in batches of 8
        for i in range(0, len(zip_list), CONCURRENCY):

            batch = zip_list[i:i+CONCURRENCY]
            print(f"\n🚀 Processing batch: {batch}")

            tasks = [scrape_zip(z, pw) for z in batch]
            results = await asyncio.gather(*tasks)

            for r in results:
                final_rows.extend(r)

    # Save CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["zip", "url", "price_chf", "rooms", "area_m2"])
        w.writerows(final_rows)

    print(f"\n✅ DONE! Saved {len(final_rows)} rows to {OUTPUT_CSV}")


# -----------------------------------------
# Entry point
# -----------------------------------------
if __name__ == "__main__":
    asyncio.run(run_all())
