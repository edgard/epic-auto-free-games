#!/usr/bin/env python3
"""
Get free games from EPIC store
"""

import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.environ.get("APP_PASSWORD")
USER_AGENT = os.environ.get("APP_USER_AGENT") or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"

def xpath_soup(element):
    """find the xpath of a given soup object"""
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(child.name if len(siblings) == 1 else "%s[%d]" % (child.name, next(i for i, s in enumerate(siblings, 1) if s is child)))
        child = parent
    components.reverse()
    return "/%s" % "/".join(components)


def get_game(browser):
    """get the game"""
    time.sleep(7)
    # Re-get the source so that we can look for any "Continue" buttons
    html = BeautifulSoup(browser.page_source, "lxml")
    try:
        spans = html.find_all("span")
        # Check for a "Continue" button for the 18+ games. If we find it, click it
        for span in spans:
            if span.get_text().upper() == "CONTINUE":
                # Get the xpath
                xpath = xpath_soup(span)
                # Use the xpath to grab the browser element (so we can click it)
                age_agree = browser.find_element_by_xpath(xpath)
                age_agree.click()
                break
        time.sleep(7)
    except:
        print()

    # Get the source again, just incase we came from clicking the potential "Continue" button
    html = BeautifulSoup(browser.page_source, "lxml")

    # Get all the button tags so we can see whether we need to grab the game or leave
    buttons = html.find_all("button")

    for button in buttons:
        if button.get_text().upper() == "OWNED":
            break
        if button.get_text().upper() == "GET":
            # Get the xpath of this button
            xpath = xpath_soup(button)
            # Use the xpath to grab the browser element (so we can click it)
            browser_element = browser.find_element_by_xpath(xpath)
            browser_element.click()
            time.sleep(4)

            # Re-get the source (again)
            html = BeautifulSoup(browser.page_source, "lxml")
            # Get all the spans so we can get the "Place Order" button
            spans = html.find_all("span")

            for span in spans:
                if span.get_text().upper() == "PLACE ORDER":
                    # Get the xpath
                    xpath = xpath_soup(span)
                    # Use the xpath to grab the browser element (so we can click it)
                    purchase_button_element = browser.find_element_by_xpath(xpath)
                    # Create object and add it to the list
                    purchase_button_element.click()
                    break
            # If the EULA prompt shows up, click it
            try:
                browser.find_element_by_xpath("""//span[contains(text(),'I Agree')]""")
            except:
                print()
            else:
                eula_agree = browser.find_element_by_xpath("""//span[contains(text(),'I Agree')]""")
                eula_agree.click()
                time.sleep(2)
            # We only want the first one (usually the game), so leave
            break


def main():
    """get free games from epic store"""

    # Main store page for Epic Games Store
    web_path = """https://www.epicgames.com/store/en-US"""

    # We will use the user-agent to trick the website into thinking we are a real person. This usually subverts most basic security
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--user-agent="{}"'.format(USER_AGENT))

    # Setup the browser object to use our modified profile
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(web_path + "/login")

    # Give the page enough time to load before we enter anything
    time.sleep(5)

    # Let's login and get that out of the way
    fill_out_user = browser.find_element_by_id("usernameOrEmail")
    fill_out_user.send_keys(USERNAME)

    fill_out_pass = browser.find_element_by_id("password")
    fill_out_pass.send_keys(PASSWORD)

    fill_out_pass.submit()
    time.sleep(8)

    # Go back to the store page
    browser.get(web_path)
    # Give the page enough time to load before grabbing the source text
    # If you get any weird errors related to 'root' or anything, start here and adjust the time
    time.sleep(4)

    # Grab the source text, and make a beautiful soup object
    html = BeautifulSoup(browser.page_source, "lxml")

    # Check for, and close, the cookies banner
    try:
        browser.find_element_by_xpath("""/html/body/div/div/div[4]/header/div/button/span""")
    except:
        print()
    else:
        cookies = browser.find_element_by_xpath("""/html/body/div/div/div[4]/header/div/button/span""")
        cookies.click()
        time.sleep(2)

    # Check for, and close, the eu cookies banner
    try:
        browser.find_element_by_xpath("""/html/body/div/div/div[4]/header/header/div/button/span""")
    except:
        print()
    else:
        cookies = browser.find_element_by_xpath("""/html/body/div/div/div[4]/header/header/div/button/span""")
        cookies.click()
        time.sleep(2)

    # Get all the span tags to make sure we get every available game
    spans = html.find_all("span")

    # Create a list for all the game dictionaries
    games = []
    for span in spans:
        if span.get_text().upper() == "FREE NOW":
            # Get the xpath
            xpath = xpath_soup(span)
            # Use the xpath to grab the browser element (so we can click it)
            browser_element = browser.find_element_by_xpath(xpath)
            # Create object and add it to the list
            games.append({"xpath": xpath, "element": browser_element})

    # Go thru each game we found and get it!
    for index, game in enumerate(games):
        game["element"].click()
        get_game(browser)
        # Go back to the store page to get the other game
        browser.get(web_path)
        # Give the page enough time to load before grabbing the source text
        time.sleep(5)
        # Selenium complains this object no longer exists, so we need to re-get it so it doesn't explode
        try:
            games[index + 1]["element"] = browser.find_element_by_xpath(games[index + 1]["xpath"])
        except:
            break

    # Close everything
    browser.quit()


# entrypoint
if __name__ == "__main__":
    main()
