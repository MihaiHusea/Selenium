import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('http://orteil.dashnet.org/experiments/cookie/')
driver.maximize_window()

time_to_check_upgrades = 5
five_minutes = 300
start = time.time()

cookies_per_second = driver.find_element(By.ID, 'cps')

cookie_button = driver.find_element(By.ID, 'cookie')

while time_to_check_upgrades < five_minutes:

    cookie_button.click()

    passed_time = time.time() - start

    if passed_time >= time_to_check_upgrades:

        upgrades = driver.find_elements(By.CSS_SELECTOR, "#store >div:not(.grayed)")

        if len(upgrades) > 0:
            upgrades[-1].click()

        time_to_check_upgrades += 5

print(cookies_per_second.text)
