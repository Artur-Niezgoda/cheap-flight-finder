from environs import Env
from datetime import datetime, timedelta
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

# Read environment variables from env file
env = Env()
env.read_env()

# iata code for origin city
ORIGIN_CITY_IATA = "BCN"

# create objects
data_manager = DataManager()
data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in data:
    # if there are no IATA codes, fetch for them
    if destination["iataCode"] == "":
        destination["iataCode"] = flight_search.get_iata(destination["city"])

    # search for the cheap flight for a given destination
    flight = flight_search.search_flight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    # if the price is lower than average, send an email
    if flight is not None and flight.price < destination["lowestPrice"]:
        notification_manager.send_email(message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-"
                                               f"{flight.origin_airport} to {flight.destination_city}-"
                                               f"{flight.destination_airport}, from {flight.out_date} to"
                                               f" {flight.return_date} with {flight.airline}.")

data_manager.destination_data = data
data_manager.update_data()

