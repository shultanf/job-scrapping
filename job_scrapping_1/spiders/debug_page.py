import asyncio
from playwright.async_api import async_playwright

async def debug_page(playwright, url):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await browser.new_page()

    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_selector("div[data-glints-tracking-element-name='job_card']", timeout=10000)
    # await page.wait_for_timeout(3000)
    html = await page.content()

    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    await context.close()
    await browser.close()
    
async def main():
    async with async_playwright() as p:
        url = 'https://glints.com/id/opportunities/jobs/explore?keyword=data&country=ID&locationName=All+Cities%2FProvinces&lowestLocationLevel=1&yearsOfExperienceRanges=NO_EXPERIENCE%2CFRESH_GRAD%2CLESS_THAN_A_YEAR'
        await debug_page(p, url)

asyncio.run(main())