import requests
from bs4 import BeautifulSoup
import re
from uuid import uuid4
from datetime import datetime
from pytz import timezone
from typing import Dict
from models.model import Model


class Cofi(Model):
    """
    Create instances of Cost of Fund Index and interact with collection cofis.
    """
    collection = 'cofis'

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        super().__init__(name, date, rate, _id)

    @classmethod
    def load_rates(cls) -> None:
        """
        Load Cost of Fund Index.
        """
        url = 'https://www.farmermac2.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all(class_="row cofi-ann")

        # Find and clean names
        names = re.findall(r'[A-Z].*:', str(data))
        names_format = [name[:-1].replace('&amp;', '&') for name in names]

        # Find rates
        rates = re.findall(r'\d+\.\d+%', str(data))

        for name, rate in zip(names_format, rates):
            cofi = cls(name, datetime.now(
                timezone('US/Eastern')).strftime("%m/%d/%Y"), rate)

            # Delete old cofi if it exists and the rate is different.
            try:
                old_cofi = cls.find_one_by(name=cofi.name)
                if old_cofi.rate != cofi.rate:
                    old_cofi.delete_from_mongo()
                    cofi.save_to_mongo()
            # Old cofi was not found.
            except:
                cofi.save_to_mongo()

    def json(self) -> Dict:
        return {"_id": self._id,
                "name": self.name,
                "date": self.date,
                "rate": self.rate}
