from common.data_collection import DataCollection
from typing import Dict
from models.model import Model


class Mortgage(Model):
    """
    Create instances of mortgages and interact with collection mortgages.
    """
    collection = 'mortgages'

    def __init__(self, frm_30yr: str, frm_15yr: str, frm_5yr: str, name: str, date: str, _id: str = None) -> None:
        self.frm_30yr = frm_30yr
        self.frm_15yr = frm_15yr
        self.frm_5yr = frm_5yr
        super().__init__(name, date, _id)

    @classmethod
    def load_rates(cls):
        """
        Load mortgages.
        """
        dates, rates = DataCollection.collect_mortgage()

        # Create mortgage instance for each row.
        for i, rate in enumerate(rates, start=1):
            d = 0 if i <= 3 else 1
            if i % 3 == 1:
                mortgage = cls(*([r + '%' for r in rate] +
                                 ['Average Rates', dates[d]]))
            elif i % 3 == 2:
                mortgage = cls(*(rate + ['Fees & Points', dates[d]]))
            else:
                mortgage = cls(*(rate + ['Margin', dates[d]]))

            # Delete old mortgage if it exists and any rate is different.
            try:
                old_mortgage = cls.find_one_by(
                    date=mortgage.date, name=mortgage.name)
                if not (old_mortgage.frm_30yr == mortgage.frm_30yr
                        and old_mortgage.frm_15yr == mortgage.frm_15yr
                        and old_mortgage.frm_5yr == mortgage.frm_5yr):
                    old_mortgage.delete_from_mongo()
                    mortgage.save_to_mongo()
            # Old mortgage was not found.
            except:
                mortgage.save_to_mongo()

    def json(self) -> Dict:
        return {"_id": self._id,
                "name": self.name,
                "date": self.date,
                "frm_30yr": self.frm_30yr,
                "frm_15yr": self.frm_15yr,
                "frm_5yr": self.frm_5yr}
