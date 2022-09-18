"""
Module responsible for creating an object that holds important data about the flight
"""


class FlightData:
    """Class fir managing flight data
    """
    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date,
                 airline) -> None:
        """
        Constructor of the class object
        :param price: price of the flight
        :param origin_city: IATA code of the origin city
        :param origin_airport:  IATA code of the origin airport
        :param destination_city: IATA code of the destination city
        :param destination_airport: IATA code of the destination airport
        :param out_date: the date of the outbound flight
        :param return_date: the date of the returning flight
        :param airline: the IATA code of the airline
        """

        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.airline = airline
