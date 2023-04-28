import time

from booking.booking import Booking

with Booking() as bot:  # control close/open browser
    bot.land_first_page()
    bot.manage_cookie_preferences(decision="Decline")
    time.sleep(2)
    bot.change_currency(selected_currency="RON")
    bot.select_place_to_go(input("Where would you like to go?\n"))
    time.sleep(2)
    bot.select_dates(check_in_date=input("Enter check-in date:(yyyy-mm-dd)\n"),
                     check_out_date=input("Enter check-out date:(yyyy-mm-dd)\n"))
    time.sleep(2)
    bot.select_number_of_guests(count=int(input("How many people?\n")))
    time.sleep(2)
    bot.search()
    time.sleep(2)
    bot.apply_filter()
    bot.refresh()  # A workaround to let our bot get the data properly
    bot.report_results()
    time.sleep(2)
