import asyncio
import os
import subprocess
from playwright.async_api import async_playwright, expect

async def run_verification():
    async with async_playwright() as p:
        server_process = subprocess.Popen(
            ['python', '-m', 'http.server', '8000'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await asyncio.sleep(2)

        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            await page.goto('http://localhost:8000')
            await expect(page.locator('.event-trigger').first).to_be_visible(timeout=15000)

            aurora_card = page.locator('.event-trigger', has_text='Aurora Dwarf Civil War').first
            modal_title = page.locator('#modal-title')

            await aurora_card.click()
            await expect(modal_title).to_have_text('Aurora Dwarf Civil War', timeout=5000)
            print("Modal opened successfully via event delegation.")

            close_btn = page.locator('#modal-close-btn')
            await close_btn.click()

            await expect(modal_title).not_to_be_visible(timeout=5000)

            # test sub event
            search_input = page.locator('#search-input')
            await search_input.fill('Pirates!')
            await asyncio.sleep(1)

            pirates_card = page.locator('.event-trigger', has_text='Pirates!').first
            sub_event = pirates_card.locator('.sub-event-trigger').first
            await sub_event.click()

            await expect(modal_title).not_to_have_text('Pirates!', timeout=5000)
            print("Sub-event modal opened successfully via event delegation.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
            server_process.kill()

if __name__ == '__main__':
    asyncio.run(run_verification())
