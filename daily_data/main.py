from playwright.sync_api import sync_playwright, Playwright
from datetime import datetime

URL = "https://www.bseindia.com/"

month_dict = {
    "1":'0',
    "2":'1',
    "3":'2',
    "4":'3',
    "5":'4',
    "6":'5',
    "7":'6',
    "8":'7',
    "9":'8',
    "10":'9',
    "11":'10',
    "12":'11',
}

filename = f"trade_hist_{datetime.now().strftime('%Y-%m-%d')}.csv"
YEAR = str(datetime.now().year)
MONTH = month_dict[str(datetime.now().month)]
FROM_DATE = '1'
TO_DATE = str(datetime.now().day)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # open new page
    page = context.new_page()
    page.goto(URL)
    page.wait_for_load_state("networkidle")

    page.get_by_role("link", name="Markets", exact=True).click()
    page.wait_for_load_state("networkidle")

    page.get_by_role("link", name="Equity").click()
    page.wait_for_load_state("networkidle")

    page.get_by_role("link", name="Historical Data").click()
    page.wait_for_load_state("networkidle")

    page.get_by_role("button", name="Equity −").click()
    page.wait_for_load_state("networkidle")

    page.get_by_role("listitem").filter(has_text="Daywise Trading Highlights (Incl Advances, Declines, Stocks on Upper / Lower Cir").get_by_role("link", name="Daywise Trading Highlights").click()

    # ---------------------
    page.wait_for_load_state("networkidle")

    page.evaluate("() => window.scroll(0, document.body.scrollHeight)")

    page.locator("#ContentPlaceHolder1_txtDate").click()
    page.get_by_role("combobox", name="Select year").select_option(YEAR)
    page.get_by_role("combobox", name="Select month").select_option(MONTH)
    page.get_by_role("link", name="1", exact=True).click()

    page.locator("#ContentPlaceHolder1_txtToDate").click()
    page.get_by_role("combobox", name="Select year").select_option(YEAR)
    page.get_by_role("combobox", name="Select month").select_option(MONTH)
    page.get_by_role("link", name=TO_DATE).click()
    page.get_by_role("button", name="Submit").click()

    with page.expect_download() as download_info:
        page.locator("#ContentPlaceHolder1_btnDownload").click()
    download = download_info.value
    download.save_as(filename)

    # page.screenshot(path="daily_2.png", full_page=True)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
