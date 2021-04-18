import requests
from bs4 import BeautifulSoup
import re
from uuid import uuid4
from datetime import datetime
from typing import Dict
from models.model import Model


class PrimeRate(Model):
    """
    Create instances of prime rates and interact with collection prime_rates.
    """
    collection = 'prime_rates'

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        super().__init__(name, date, rate, _id)

    @classmethod
    def load_rates(cls) -> None:
        """
        Loan prime rates.
        """
        url = 'https://www.hsh.com/indices/prime-rate.html'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = str(soup.find_all(class_='prime-data')[0])

        dates = re.findall(r'\d{2}-[a-zA-z]{3}-\d{2}', text)
        format_dates = [datetime.strptime(
            date, '%d-%b-%y').strftime('%m/%d/%Y') for date in dates]

        rates = re.findall(r'\d+\.\d+%', text)

        for date, rate in zip(format_dates, rates):
            prime_rate = cls('prime_rate', date, rate)

            # Delete prime rates if it exists and the rate is different.
            try:
                old_prime_rate = cls.get_by_date(prime_rate.date)
                if old_prime_rate.rate != prime_rate.rate:
                    old_prime_rate.delete_from_mongo()
                    prime_rate.save_to_mongo()
            # Old prime rate was not found.
            except:
                prime_rate.save_to_mongo()

    def json(self) -> Dict:
        return {"_id": self._id,
                "name": self.name,
                "date": self.date,
                "rate": self.rate}
