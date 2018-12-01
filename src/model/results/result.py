import datetime
import uuid

from src.common.database import Database


class Result(object):
    def __init__(self,phone,subject,test_id,mark,date=datetime.datetime.now(),_id=None):
        self.phone = phone,
        self.subject = subject
        self.test_id = test_id
        self.mark = mark
        self.date=date
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            '_id':self._id,
            'phone':self.phone,
            'subject':self.subject,
            'test_id':self.test_id,
            'mark':self.mark,
            'date': self.date
        }

    def save_to_mongo(self):
        Database.insert('results',self.json())
        return True

    @classmethod
    def get_results_phone(cls,phone):
        results = Database.find_all('results',{'phone':phone})
        if results is not None:
            return [cls(**result) for result in results]
        return None