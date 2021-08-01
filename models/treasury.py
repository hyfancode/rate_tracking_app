from common.data_collection import DataCollection
from typing import Dict
from models.model import Model


class Treasury(Model):
    """
    Create instances of treasuries and interact with collection treasuries.
    """
    collection = 'treasuries'

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        super().__init__(name, date, rate, _id)

    @classmethod
    def load_rates(cls, name: str) -> None:
        """
        Load treasury rates.
        """
        dates_format, rates = DataCollection.collect_treasury(name)

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
