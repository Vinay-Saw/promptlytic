from playwright.sync_api import sync_playwright
import time

def render_page(url: str, headless: bool = True, timeout: int = 30):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.set_default_navigation_timeout(timeout * 1000)
        page.goto(url)
        try:
            page.wait_for_load_state("networkidle", timeout=3000)
        except Exception:
            pass
        time.sleep(0.6)
        html = page.content()
        final = page.url
        ctx.close()
        browser.close()
        return final, html
