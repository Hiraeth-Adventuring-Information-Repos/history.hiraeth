import asyncio
import os
import subprocess
from playwright.async_api import async_playwright, expect

async def run_verification():
    """Connects to the app and verifies navigation functionality."""
    async with async_playwright() as p:
        # Start server
        server_process = subprocess.Popen(
            ['python', '-m', 'http.server', '8000'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await asyncio.sleep(2)  # Give server time to start

        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            print("Navigating to http://localhost:8000...")
            await page.goto('http://localhost:8000')

            print("Waiting for timeline to load...")
            # Correctly wait for the first event trigger to be visible
            await expect(page.locator('.event-trigger').first).to_be_visible(timeout=15000)
            print("Timeline loaded.")

            # Define the locators
            piracy_card = page.locator('.event-trigger', has_text='Pirates!').first
            modal_title = page.locator('#modal-title')

            print("Testing modal opening...")
            await piracy_card.scroll_into_view_if_needed()
            await piracy_card.click() # Correctly awaited action
            await expect(modal_title).to_have_text('Pirates!', timeout=5000)
            print("Modal opened to 'Pirates!'.")

            print("Testing sub-event opening from modal...")
            # Target the sub-event inside the modal to avoid pointer interception
            sub_event = page.locator('#modal-content .sub-event-trigger', has_text='The Sinking of the Gilded Lily').first
            await expect(sub_event).to_be_visible(timeout=5000)
            # click on the sub event trigger
            await sub_event.click()
            await expect(modal_title).to_have_text('The Sinking of the Gilded Lily', timeout=5000)
            print("Sub-event opened.")

            print("Testing modal close...")
            await page.locator('#modal-close-btn').click()
            await expect(page.locator('#modal-container')).to_be_hidden(timeout=5000)
            print("Modal closed.")

            print("Verification successful!")

        except Exception as e:
            print(f"An error occurred during verification: {e}")
        finally:
            await browser.close()
            server_process.kill()
            print("Server stopped.")

if __name__ == '__main__':
    asyncio.run(run_verification())
