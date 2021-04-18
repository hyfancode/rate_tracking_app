import requests
from bs4 import BeautifulSoup
import re
from uuid import uuid4
from datetime import datetime
from typing import Dict
from models.model import Model


class Mirs(Model):
    """
    Create instances of MIRS transition index and interact with collection mirses.
    """
    collection = 'mirses'

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        super().__init__(name, date, rate, _id)

    @classmethod
    def load_rates(cls) -> None:
        """
        Load MIRS transition indexes.
        """
        url = 'https://www.fhfa.gov/DataTools/Downloads/Pages/Monthly-Interest-Rate-Data.aspx'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all(
            class_=['ms-rteTableOddRow-4', 'ms-rteTableEvenRow-4'])

        dates = re.findall(r'[A-Z][a-z]+ 202\d{1}', str(data))
        dates_format = [datetime.strptime(
            date, '%B %Y').strftime('%m/%Y') for date in dates]

        rates = re.findall(r'\d+\.\d+', str(data))[:len(dates)]

        for date, rate in zip(dates_format, rates):
            mirs = cls('MIRS Transition Index', date, rate)

            # Delete old mirs if it exists and the rate is different.
            try:
                old_mirs = cls.get_by_date(mirs.date)
                if old_mirs.rate != mirs.rate:
                    old_mirs.delete_from_mongo()
                    mirs.save_to_mongo()
            # Old mirs was not found.
            except:
                mirs.save_to_mongo()

    def json(self) -> Dict:
        return {"_id": self._id,
                "name": self.name,
                "date": self.date,
                "rate": self.rate}
