"""
Module responsible for Flight related searches

Class:
    FlightSearch

Methods:
    get_iata
        Get IATA code for the given city name
    search_flight

"""

from environs import Env
import requests
from flight_data import FlightData

env = Env()
env.read_env()
api_endpoint = "https://api.tequila.kiwi.com/"
headers = {
    "apikey": env("TEQUILA_API")
}


class FlightSearch:
    """This class is responsible for talking to the Flight Search API"""

    @staticmethod
    def get_iata(city_name: str) -> str:
        """
        Get IATA code for the given city name
        :param city_name: string containing name of the city
        :return: string IATA code of the city
        """

        code_endpoint = f"{api_endpoint}locations/query"
        parameters = {
            "term": city_name, "location_types": "city"
        }
        results = requests.get(url=code_endpoint, params=parameters, headers=headers)
        locations = results.json()["locations"][0]

        return locations["code"]

    @staticmethod
    def search_flight(origin_city_code: str, destination_city_code: str, from_time: str, to_time: str) -> object:
        """
        Search flight according to given parameters
        :param origin_city_code: code for the city of origin
        :param destination_city_code: code for the destination city
        :param from_time: tomorrow's date
        :param to_time: 6 months after tomorrow
        :return: an object of the FlightData class
        """

        search_endpoint = f"{api_endpoint}v2/search"
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD",
            "select_airlines": "FR,W6",
            "select_airlines_exclude": True
        }

        response = requests.get(url=search_endpoint, params=query, headers=headers)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
            airline=data["route"][0]["airline"]
        )
        print(f"{flight_data.destination_city}: ${flight_data.price}")

        return flight_data
