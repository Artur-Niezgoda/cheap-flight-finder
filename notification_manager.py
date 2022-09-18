"""
Module that sends an email when the cheap flight is found

Classes:
    NotificationManager

Methods:
    send_email(message)
        send the message to the given email
"""

from environs import Env
import smtplib
# Read environment variables from env file
env = Env()
env.read_env()


class NotificationManager:
    """Class that sends an email to a single given email address"""
    def __init__(self):
        """
        Constructor of the class
        Attributes:
            my_email (string): email address from which the email will be send (saved in .env file)
            password (string): password generated for the email address (saved in .env file)
            to_email (string): email to which the notification will be sent (saved in .env file)

        """

        self.my_email = env("MY_EMAIL")
        self.password = env("PASSWORD_EMAIL")
        self.to_email = env("TO_EMAIL")

    def send_email(self, message: str) -> None:
        """
        Function that sends an email to notify about the cheap flight
        :param message: string containing the message
        """

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.my_email, self.password)
            connection.sendmail(
                from_addr=self.my_email,
                to_addrs=self.to_email,
                msg=message
            )
        print("An email has been sent.")
