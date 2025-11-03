import asyncio
import os
import subprocess
from playwright.async_api import async_playwright, expect

async def run_verification():
    """Connects to the app and verifies navigation functionality."""
    # Ensure the scratch directory exists
    verification_dir = '/home/swebot/jules-scratch/verification'
    os.makedirs(verification_dir, exist_ok=True)
    screenshot_path = os.path.join(verification_dir, 'navigation_verify.png')

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
            await expect(page.locator('.event-trigger').first()).to_be_visible(timeout=15000)
            print("Timeline loaded.")

            # Define the locators
            aurora_card = page.locator('.event-trigger', has_text='Aurora Dwarf Civil War').first()
            modal_title = page.locator('#modal-title')
            next_btn = page.locator('#modal-next-btn')
            prev_btn = page.locator('#modal-prev-btn')

            print("Testing modal opening...")
            await aurora_card.scroll_into_view_if_needed()
            await aurora_card.click() # Correctly awaited action
            await expect(modal_title).to_have_text('Aurora Dwarf Civil War', timeout=5000)
            print("Modal opened to 'Aurora Dwarf Civil War'.")

            print("Testing 'next' navigation...")
            await next_btn.click() # Correctly awaited action
            await expect(modal_title).to_have_text('The Stars Fall', timeout=5000)
            print("Navigation to 'The Stars Fall' successful.")

            print("Testing 'previous' navigation...")
            await prev_btn.click() # Correctly awaited action
            await expect(modal_title).to_have_text('Aurora Dwarf Civil War', timeout=5000)
            print("Navigation back to 'Aurora Dwarf Civil War' successful.")

            print(f"Taking screenshot: {screenshot_path}")
            await page.screenshot(path=screenshot_path) # Correctly awaited action
            print("Verification successful!")

        except Exception as e:
            print(f"An error occurred during verification: {e}")
        finally:
            await browser.close()
            server_process.kill()
            print("Server stopped.")

if __name__ == '__main__':
    asyncio.run(run_verification())
