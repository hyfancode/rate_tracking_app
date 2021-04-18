from datetime import date
import requests
from bs4 import BeautifulSoup
from uuid import uuid4
from datetime import datetime
from pytz import timezone
from typing import Dict
from models.model import Model


class Log(Model):
    """
    Create log instances and interact with collection logs.
    """
    collection = 'logs'

    def __init__(self, username: str, action: str, date_time: str = None, _id: str = None) -> None:
        self.username = username
        self.action = action
        self.date_time = date_time or datetime.now(
            timezone('US/Eastern')).strftime("%m/%d/%Y %H:%M:%S")
        self._id = _id or uuid4().hex

    def json(self) -> Dict:
        return {"_id": self._id,
                "date_time": self.date_time,
                "username": self.username,
                "action": self.action}
