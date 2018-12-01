import uuid

from src.common.database import Database

class Exam():
    def __init__(self,student_id,test_id,subject_id,mark=0,_id=None):
        self.id = uuid.uuid4().hex if _id is None else _id
        self.student_id = student_id
        self.test_id= test_id
        self.subject_id=subject_id
        self.mark=mark

    def json(self):
        return {
            "student_id":self.student_id,
            "test_id":self.test_id,
            "subject_id":self.subject_id,
            "mark":self.mark,
            "_id":self.id
        }

    def save_to_mango(self):
        Database.insert(collection="exams", data=self.json())

    @classmethod
    def get_exam(cls, id):
        exam = Database.find_one({"student_id": id})
        return cls(exam)

