from abc import ABCMeta, abstractmethod
from typing import List, Dict, TypeVar, Type
from uuid import uuid4
from datetime import datetime
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from common.database import Database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):
    """
    Model class has common methods for the subclasses.
    """
    collection: str

    def __init__(self, name: str, date: str, rate: str, _id: str = None) -> None:
        self.name = name
        self.date = date
        self.rate = rate
        self._id = _id or uuid4().hex

    @abstractmethod
    def json(self) -> Dict:
        """
        json method needs to be initialized in the subclass.
        """
        raise NotImplementedError

    def save_to_mongo(self) -> None:
        """
        Save data to mongodb.
        """
        Database.update_one(self.collection, {"_id": self._id}, self.json())

    def delete_from_mongo(self) -> None:
        """
        Delete data from mongodb.
        """
        Database.delete_one(self.collection, {"_id": self._id})

    @classmethod
    def find_all(cls: Type[T]) -> List[T]:
        """
        Find all elements in the collection.
        """
        elements = Database.find(cls.collection, {})
        return [cls(**element) for element in elements]

    @classmethod
    def find_one_by(cls: Type[T], **query: str) -> T:
        """
        Find an element by query.
        """
        return cls(**Database.find_one(cls.collection, query))

    @classmethod
    def find_many_by(cls: Type[T], **query: str) -> List[T]:
        """
        Find a list of elements by query.
        """
        return [cls(**element) for element in Database.find(cls.collection, query)]

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        """
        Find an element by unique id.
        """
        return cls.find_one_by(_id=_id)

    @classmethod
    def get_by_date(cls: Type[T], date: "Date") -> T:
        """
        Find an element by the date.
        """
        return cls.find_one_by(date=date)

    @classmethod
    def create_plot(cls: Type[T], name: str) -> str:
        """
        Search MongoDB and return data with json format.
        """
        dates, rates = [], []
        elements = cls.find_many_by(name=name)

        date_str = '%m/%Y' if name == 'MIRS Transition Index' else '%m/%d/%Y'

        elements_sorted = sorted(
            elements, key=lambda element: datetime.strptime(element.date, date_str), reverse=True)

        # Show 20 records
        for element in elements_sorted[:20]:
            dates.append(datetime.strptime(element.date, date_str))
            rates.append(float(element.rate.replace('%', '')))

        df = pd.DataFrame({'dates': dates,
                           'rates': rates})
        # Customize color
        colors = {'Libor': '#1F77B4', 'PrimeRate': '#00CC96',
                  'Mirs': '#862A16', 'Treasury': '#FFA15A'}
        color = colors[cls.__name__]

        data = [
            go.Scatter(
                x=df['dates'],
                y=df['rates'],
                mode='lines+markers',
                name=name,
                line={'color': color})
        ]

        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
