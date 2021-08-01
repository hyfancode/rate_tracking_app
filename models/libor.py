from common.data_collection import DataCollection
from typing import Dict
from models.model import Model


class Libor(Model):
    """
    Create instances of libors and interact with collection libors.
    """
    collection = 'libors'

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        super().__init__(name, date, rate, _id)

    @classmethod
    def load_rates(cls, name: str) -> None:
        """
        Load libor rates.
        """
        libors = DataCollection.collect_libor(name)

        for date, rate in libors:
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
