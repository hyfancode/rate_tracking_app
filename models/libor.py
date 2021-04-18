import requests
from bs4 import BeautifulSoup
from uuid import uuid4
from datetime import datetime
from typing import Dict
from models.model import Model


class Libor(Model):
    """
    Create instances of libors and interact with collection libors.
    """
    collection = 'libors'
    libors = ['overnight', '1-week', '1-month',
              '3-months', '6-months', '12-months']

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        super().__init__(name, date, rate, _id)

    @classmethod
    def load_rates(cls, name: str) -> None:
        """
        Load libor rates.
        """
        NUM_OF_DAY = 12  # 12 current interest rates on the page

        if name not in cls.libors:
            raise NameError('The libor name is invalid.')

        url = f'https://www.global-rates.com/interest-rates/libor/american-dollar/usd-libor-interest-rate-{name}.aspx'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all(
            ['tr', 'td'], {'class': ['tabledata1', 'tabledata2']})

        for d in data[:NUM_OF_DAY]:
            info = d.get_text().strip().replace(u'\xa0', u' ').split('\n')

            date = datetime.strptime(info[0].title(), '%B %d %Y').strftime(
                '%m/%d/%Y')
            rate = info[1].replace(' ', '')
            libor = cls(name, date, rate)

            # Delete old libor if it exists and the rate is different.
            try:
                old_libor = cls.find_one_by(date=libor.date, name=libor.name)
                if old_libor.rate != libor.rate:
                    old_libor.delete_from_mongo()
                    libor.save_to_mongo()
            # Old libor was not found.
            except:
                libor.save_to_mongo()

    def json(self) -> Dict:
        return {"_id": self._id,
                "name": self.name,
                "date": self.date,
                "rate": self.rate}
