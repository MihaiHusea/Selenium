"""
This file is going to include method that will parse the specific
data that we need from each one of deal boxes
"""
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, boxes_section_element):
        self.boxes_section_element = boxes_section_element

    def pull_deal_box_attributes(self):
        data_collection = []

        for deal_box in self.boxes_section_element:
            # Pulling the hotel name
            hotel_name = deal_box.find_element(By.CLASS_NAME, 'fcab3ed991.a23c043802').get_attribute(
                'innerHTML').strip()

            # Pulling the hotel price
            hotel_price = deal_box.find_element(By.CSS_SELECTOR,
                                                'span[data-testid="price-and-discounted-price"]').get_attribute(
                'innerHTML').strip().replace("&nbsp;", " ")

            # Pulling the hotel score

            try:
                score_element = WebDriverWait(deal_box, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="b5cd09854e d10a6220b4"]')))
                hotel_score = score_element.get_attribute('innerHTML').strip()
            except TimeoutException:
                hotel_score = 'Not available'

            data_collection.append([hotel_name, hotel_price, hotel_score])
        return data_collection
