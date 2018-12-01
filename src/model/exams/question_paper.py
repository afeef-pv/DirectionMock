import uuid
import pickle
from bson.binary import Binary
from src.common.database import Database

Database.initilize()

class Questions():
    def __init__(self,course,subject,test_id,questions=[],_id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.course=course
        self.subject = subject
        self.test_id=test_id
        if type(questions) is not list:
            questions = pickle.loads(questions)
        self.questions = questions

    def add_question(self,q):
        self.questions.append(q)

    def json(self):
        questions=pickle.dumps(self.questions)
        return {
            "_id":self._id,
            "course":self.course,
            "subject":self.subject,
            "test_id":self.test_id,
            "questions":Binary(questions)
        }

    def save_to_mongo(self):
        Database.insert("questions",self.json())

    @classmethod
    def get_questions(cls,course):
        data = Database.find_all("questions",{'course':course})
        return [cls(**question) for question in data]

    @classmethod
    def get_questions_by_id(cls, id):
        data = Database.find_one("questions", {'_id': id})
        return cls(**data)

    @classmethod
    def get_all_questions_by_test_id(cls, id):
        data = Database.find_all("questions", {'test_id': id})
        return [cls(**paper) for paper in data]

    @staticmethod
    def remove_test_questions(id):
        Database.remove("questions",{'_id':id})




