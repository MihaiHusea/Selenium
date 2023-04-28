import booking.constants as const
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver=webdriver.Chrome(service=Service(ChromeDriverManager().install())), teardown=False):
        super(Booking, self).__init__()
        self.driver = driver
        self.teardown = teardown
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def manage_cookie_preferences(self, decision=None):
        if decision == "Accept":
            self.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        else:
            self.find_element(By.ID, 'onetrust-reject-all-handler').click()

    def change_currency(self, selected_currency=None):
        currency_button = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_button.click()

        currencies = self.find_elements(By.CLASS_NAME, "ccff2b4c43.ea27cffb06")
        for currency in currencies:
            if selected_currency in currency.text:
                currency.click()
                break

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, ':Ra9:')
        search_field.clear()
        search_field.send_keys(place_to_go)
        result = self.find_element(By.CSS_SELECTOR, '.a80e7dc237:nth-child(1) .a40619bfbe')
        result.click()

    def select_dates(self, check_in_date, check_out_date, mounts_from_now=None):

        if mounts_from_now:
            go_next_mounts = self.find_element(By.CLASS_NAME,
                                               'fc63351294.a822bdf511.e3c025e003.fa565176a8.cfb238afa1.c334e6f658.ae1678b153.c9fa5fc96d.be298b15fa')
            for item in range(mounts_from_now):
                go_next_mounts.click()

        check_in_element = self.find_element(By.CSS_SELECTOR,
                                             f'span[data-date="{check_in_date}"]')
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR,
                                              f'span[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_number_of_guests(self, count):
        selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection_element.click()

        # Set the adults number to minimum value (=1)
        while True:
            decrease_adults_elements = self.find_element(By.CSS_SELECTOR, '.e1b7cfea84:nth-child(1)')
            decrease_adults_elements.click()

            # condition: if adults value reaches 1 break the while loop:

            adult_value_element = self.find_element(By.ID, 'group_adults')

            adult_value = adult_value_element.get_attribute('value')  # get the adult count
            if int(adult_value) == 1:
                break

        increase_button_element = self.find_element(By.CSS_SELECTOR,
                                                    '.b2b5147b20:nth-child(1) .fc63351294:nth-child(3)')
        for _ in range(count - 1):  # we have to subtract 1 because minimum adults value is 1
            increase_button_element.click()

    def search(self):
        search_element = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_element.click()

    def apply_filter(self, *filter_by_nr_of_stars):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(*filter_by_nr_of_stars)
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Price", "Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
