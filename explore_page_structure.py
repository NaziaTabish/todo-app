"""Script to explore the actual page structure of the Todo application."""

import asyncio
from playwright.async_api import async_playwright

async def explore_page_structure():
    """Explore the actual page structure of the Todo application."""

    print("Exploring Todo Application Page Structure...")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set to True if you want headless
        page = await browser.new_page()

        try:
            # Navigate to the application
            print("Navigating to http://localhost:3000...")
            await page.goto("http://localhost:3000")

            # Wait for page to load
            await page.wait_for_timeout(3000)

            # Get all available links on the page
            links = await page.query_selector_all("a")
            print(f"\nFound {len(links)} links on the page:")
            for i, link in enumerate(links):
                link_text = await link.inner_text()
                link_href = await link.get_attribute("href")
                print(f"  {i+1}. '{link_text.strip()}' -> {link_href}")

            # Get all buttons
            buttons = await page.query_selector_all("button")
            print(f"\nFound {len(buttons)} buttons on the page:")
            for i, button in enumerate(buttons):
                button_text = await button.inner_text()
                print(f"  {i+1}. '{button_text.strip()}'")

            # Get all input fields
            inputs = await page.query_selector_all("input")
            print(f"\nFound {len(inputs)} input fields on the page:")
            for i, input_field in enumerate(inputs):
                input_type = await input_field.get_attribute("type")
                input_name = await input_field.get_attribute("name")
                input_id = await input_field.get_attribute("id")
                print(f"  {i+1}. type='{input_type}', name='{input_name}', id='{input_id}'")

            # Get all heading elements
            headings = await page.query_selector_all("h1, h2, h3, h4, h5, h6")
            print(f"\nFound {len(headings)} heading elements on the page:")
            for i, heading in enumerate(headings):
                heading_tag = await page.evaluate("(element) => element.tagName", heading)
                heading_text = await heading.inner_text()
                print(f"  {i+1}. {heading_tag}: '{heading_text.strip()}'")

            # Get all elements with class names containing certain keywords
            auth_elements = await page.query_selector_all("*[class*='auth' i], *[class*='login' i], *[class*='register' i]")
            print(f"\nFound {len(auth_elements)} auth-related elements:")
            for i, elem in enumerate(auth_elements):
                elem_class = await elem.get_attribute("class")
                elem_text = await elem.inner_text()
                print(f"  {i+1}. class='{elem_class}', text='{elem_text.strip()[:50]}...'")

            # Get page title
            title = await page.title()
            print(f"\nPage title: {title}")

            # Wait to observe the page
            print("\nWaiting 10 seconds to observe the page...")
            await page.wait_for_timeout(10000)

        except Exception as e:
            print(f"Error during exploration: {str(e)}")
            # Take a screenshot for debugging
            await page.screenshot(path="exploration_error_screenshot.png")

        finally:
            # Close the browser
            await browser.close()
            print("\nBrowser closed.")

if __name__ == "__main__":
    asyncio.run(explore_page_structure())