import asyncio
from playwright.async_api import async_playwright
import subprocess
import os

async def run():
    server_process = subprocess.Popen(
        ['python', '-m', 'http.server', '8000'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    await asyncio.sleep(2)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://localhost:8000')
        await page.wait_for_selector('.event-trigger')

        # Search for something that won't exist
        await page.fill('#search-input', 'XyZqWrTyU')
        await asyncio.sleep(1)

        # Take screenshot
        os.makedirs('/home/swebot/jules-scratch/verification', exist_ok=True)
        await page.screenshot(path='/home/swebot/jules-scratch/verification/search_empty_new.png')

        # Click the clear search button
        await page.click('#clear-search-btn')
        await asyncio.sleep(1)

        # Take screenshot after clearing
        await page.screenshot(path='/home/swebot/jules-scratch/verification/search_cleared.png')

        await browser.close()
        server_process.kill()

asyncio.run(run())
