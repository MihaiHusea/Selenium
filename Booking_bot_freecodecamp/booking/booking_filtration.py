"""This file will include a class with instance methods, that will be responsible to interact
 with our website, after we have some results, to apply filters"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_element = self.driver.find_element(By.ID, 'filter_group_class_:R14q:')
        # In the next line we get all the child elements for star_filtration_element:
        star_child_elements = star_filtration_element.find_elements(By.CSS_SELECTOR, '*')

        for star_value in star_values:
            for element in star_child_elements:
                if str(element.get_attribute('innerHTML').strip()) == f'{star_value} stars':
                    element.click()

    def sort_price_lowest_first(self):
        selection_element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        selection_element.click()
        lowest_price_element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
        lowest_price_element.click()
