import requests
from bs4 import BeautifulSoup
import re
from uuid import uuid4
from datetime import datetime
from typing import Dict
from models.model import Model


class Treasury(Model):
    """
    Create instances of treasuries and interact with collection treasuries.
    """
    collection = 'treasuries'
    years = ['1_year', '2_year', '3_year', '5_year', '7_year', '10_year']

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        super().__init__(name, date, rate, _id)

    @classmethod
    def load_rates(cls, name: str) -> None:
        """
        Load treasury rates.
        """
        if name not in cls.years:
            raise NameError('This year is invalid.')

        url = f'https://ycharts.com/indicators/{name}_treasury_rate'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Date
        data_date = soup.find_all('td')
        dates = re.findall(r'[A-Z]{1}[a-z]+ \d+, \d{4}', str(data_date))[:50]

        # Rate
        data_rate = soup.find_all(['td'], {'class': 'text-right'})
        rates = re.findall(r'\d+\.\d+%', str(data_rate))[:50]

        dates_format = [datetime.strptime(
            d, '%B %d, %Y').strftime('%m/%d/%Y') for d in dates]

        for date, rate in zip(dates_format, rates):
            treasury = cls(name, date, rate)

            # Delete old treasury if it exists and rate is different
            try:
                old_treasury = cls.find_one_by(
                    date=treasury.date, name=treasury.name)
                if old_treasury.rate != treasury.rate:
                    old_treasury.delete_from_mongo()
                    treasury.save_to_mongo()
            # Old treasury was not found
            except:
                treasury.save_to_mongo()

    def json(self) -> Dict:
        return {"_id": self._id,
                "name": self.name,
                "date": self.date,
                "rate": self.rate}
