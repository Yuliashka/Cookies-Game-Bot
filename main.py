# FROM WEBSITE: http://orteil.dashnet.org/experiments/cookie/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chrom_driver_path = "C:\Development\chromedriver.exe"

# SHOWING A PATH:
driver = webdriver.Chrome(chrom_driver_path)


# GETTING FROM PAGE:
driver.get("http://orteil.dashnet.org/experiments/cookie/")

#GETTING COOKIE:
cookie = driver.find_element_by_id("cookie")

#GETTING UPGRATED ITEMS IDs
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]


# The time now in seconds that passed since epoch plus 5 seconds:
timeout = time.time() + 5

# The time now in seconds that passed since epoch plus 5 minutes:
one_min = time.time() + 60

while True:
    cookie.click()

    # Every 5 seconds:
    if time.time() > timeout:

        # GET ALL UPGRADE <b> TAGS:
        # In <div #store> we find all <b> tags which contains additional prices:
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []

        # CONVERT <b> TEXT INTO INT:
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        my_money = driver.find_element_by_id("money").text
        if "," in my_money:
            my_money = my_money.replace(",", "")
        cookie_count = int(my_money)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element_by_id(to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > one_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)
        break

