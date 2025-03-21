from simplex import Simplex
import os
from dotenv import load_dotenv
import time
from playwright.async_api import Page

load_dotenv()

def login():
    simplex = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    simplex.create_session(proxies=True)
    simplex.goto("https://bill.com")
    
    simplex.wait(100000)

import asyncio
from playwright.async_api import async_playwright
from hyperbrowser import AsyncHyperbrowser
from hyperbrowser.models.session import CreateSessionParams, ScreenConfig
import os
import dotenv

dotenv.load_dotenv()

async def main():
    client = AsyncHyperbrowser(api_key=os.getenv("HYPERBROWSER_API_KEY"))
    # Create a session and connect to it using Pyppeteer
    session = await client.sessions.create(
        params=CreateSessionParams(
            use_stealth=True,
            use_proxy=True,
            operating_systems=["macos"],
            device=["desktop"],
            locales=["en"],
        )
    )
    print(session.live_url)
    async with async_playwright() as p:
        
        browser = await p.chromium.connect_over_cdp(session.ws_endpoint)
        
        # Create context with permissions
        context = await browser.new_context(
        )
        import json
        page = await context.new_page()
        
        session_data = json.load(open("bill_session.json"))
        await page.goto("https://bill.com")
        await restore_session_data(page, session_data)
        await page.wait_for_timeout(10000000)
    
async def restore_session_data(page: Page, session_data: dict):
    # First set cookies
    if 'cookies' in session_data:
        await page.context.add_cookies(session_data['cookies'])
        
    # Now set localStorage
    if 'localStorage' in session_data:
        for key, value in session_data['localStorage'].items():
            await page.evaluate("""({ key, value }) => {
                localStorage.setItem(key, value);
            }""", {"key": key, "value": value})
    
    # Set sessionStorage
    if 'sessionStorage' in session_data:
        for key, value in session_data['sessionStorage'].items():
            await page.evaluate("""({ key, value }) => {
                sessionStorage.setItem(key, value);
            }""", {"key": key, "value": value})
    print("restored")
    
if __name__ == "__main__":
    asyncio.run(main())
    