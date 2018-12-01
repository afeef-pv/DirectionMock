import uuid
from src.common.database import Database


class Course():
    def __init__(self,course_id,course_name,_id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.course_id=course_id
        self.name=course_name

    def json(self):
        return {
            "course_id":self.course_id,
            "course_name":self.name,
            "_id":self._id
        }

    def save_to_mongo(self):
        Database.insert(collection='courses', data=self.json())

    @classmethod
    def get_form(cls, course_name):
        course = Database.find_one({"course_name": course_name})
        return cls(**course)