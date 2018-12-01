import datetime
import uuid

from src.common.database import Database
from src.model.exams.question_paper import Questions


class Test():
    def __init__(self,test_name,course,date=datetime.datetime.utcnow(),status="active",_id = None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.test_name = test_name
        self.course = course
        self.date = date
        self.status=status

    def json(self):
        return {
            "test_name":self.test_name,
            "course":self.course,
            "date":self.date,
            "status":self.status,
            "_id":self._id
        }

    def save_to_mongo(self):
        Database.insert("tests",self.json())

    @classmethod
    def get_test(cls, name):
        test = Database.find_one('tests',{"test_name": name})
        return cls(**test)
    @classmethod
    def get_test_by_id(cls, id):
        test = Database.find_one('tests',{"_id": id})
        return cls(**test)

    @staticmethod
    def get_tests():
        return Database.find_all('tests', {'status': 'active'})

    @staticmethod
    def get_test_by_course(course):
        return Database.find_all('tests', {'course': course, 'status': 'active'})
    @staticmethod
    def remove_test(id):
        Questions.remove_test_questions(id)
        Database.remove("tests",{'_id':id})
