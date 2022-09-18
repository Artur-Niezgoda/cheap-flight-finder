"""
Module that speaks with Sheety Api, reading and saving the data to the Google Sheet.

Classes:
    DataManager

Methods:
    get_destination_data()
        gets data from Google Sheet
    update_data()
        saves data to Google Sheet
"""

from environs import Env
import requests

# Read environment variables from env file
env = Env()
env.read_env()
sheety_id = env("SHEETY_ID")  # read users id
sheety_endpoint = f"https://api.sheety.co/{sheety_id}/flightDeals/prices"


class DataManager:
    """
    This class is responsible for talking to the Google Sheet.

    Attributes
        destination_data:
            data loaded from the Google Sheet, initiated as an empty dictionary
    """
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self) -> dict:
        """
        Get data from Google Sheet
        :return: dict containing the data
        """

        response = requests.get(url=sheety_endpoint)
        self.destination_data = response.json()["prices"]

        return self.destination_data

    def update_data(self) -> None:
        """
        Save data to Google Sheet
        :return:
        """

        for city in self.destination_data:
            updated_data = {
                "price": {
                        "iataCode": city["iataCode"],
                        }
            }
            requests.put(url=f"{sheety_endpoint}/{city['id']}",
                         json=updated_data
                        )

