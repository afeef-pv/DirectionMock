import uuid

from src.common.database import Database


class Subject():
    def __init__(self,subject_id,subject_name,course_id,_id=None):
        self.subject_id=subject_id
        self.subject_name=subject_name
        self.course_id = course_id
        self.id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "subject_id":self.subject_id,
            "subject_name":self.subject_name,
            "course_id":self.course_id,
            "_id":self.id
        }

    def save_to_mongo(self):
        Database.insert("subjects",self.json())

    @classmethod
    def get_subject(cls, subject_id):
        subject = Database.find_one('subjects',{"subject_id": subject_id})
        return cls(**subject)