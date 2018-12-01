import datetime
import uuid

from src.common.database import Database


class Form():
    def __init__(self,name,phone,_id = None,created_date=datetime.datetime.utcnow(),course = "",status="pending"):
        self.name = name
        self.phone = phone
        self._id = uuid.uuid4().hex if _id is None else _id
        self.created_date = created_date
        self.course = course
        self.status = status

    def json(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "_id": self._id,
            "created_date": self.created_date,
            "course":self.course,
            "status":self.status

        }

    def save_to_mongo(self):
        Database.insert(collection='students', data=self.json())



    @staticmethod
    def update(phone):
        Database.update("students",{"phone":phone},{"$set":{"status":"joined"}})

    @classmethod
    def get_form(cls,phone):
        form_data = Database.find_one('students',{"phone":phone})
        if form_data is None:
            return None
        return cls(**form_data)
