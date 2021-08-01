from common.data_collection import DataCollection
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
        dates_format, rates = DataCollection.collect_mirs()

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
