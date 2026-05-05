import asyncio
from playwright.async_api import async_playwright, expect
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

        # Press '/' and check if search input gets focused
        await page.keyboard.press('/')
        await asyncio.sleep(0.5)

        # Verify it's focused
        search_input = page.locator('#search-input')
        await expect(search_input).to_be_focused()

        print("Keyboard shortcut verified successfully.")

        await browser.close()
        server_process.kill()

asyncio.run(run())
