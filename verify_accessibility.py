from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8000")
    page.wait_for_timeout(500)

    # Open sidebar
    page.get_by_role("button", name="Toggle navigation menu").click()
    page.wait_for_timeout(500)

    # Check if a tag filter is visible and focusable
    page.locator("#tag-filters").get_by_text("conflict").hover()
    page.wait_for_timeout(500)

    # Take screenshot of open sidebar with tag filter hovered
    page.screenshot(path="/home/swebot/jules-scratch/verification/screenshots/verification.png")
    page.wait_for_timeout(500)

    # Press Escape to close sidebar
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/swebot/jules-scratch/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
