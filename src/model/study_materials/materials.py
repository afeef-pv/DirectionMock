import uuid

from src.common.database import Database


class Material(object):
    def __init__(self,subject,course,content,_id=None):
        self.subject = subject
        self.course = course
        self.content = content
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "subject":self.subject,
            "course":self.course,
            "content":self.content,
            "_id":self._id
        }

    def save_to_mongo(self):
        Database.insert('study_materials',self.json())
        return True

    @classmethod
    def get_materials(cls):
        datas = Database.find_all('study_materials',{})
        if datas is not None:
            return [cls(**data) for data in datas]
        return None

    @classmethod
    def get_materials_by_course(cls,course):
        datas = Database.find_all('study_materials', {'course':course})
        if datas is not None:
            return [cls(**data) for data in datas]
        return None

    @classmethod
    def get_materials_by_subject(cls, subject):
        datas = Database.find_all('study_materials', {'subject': subject})
        if datas is not None:
            return [cls(**data) for data in datas]
        return None

    @classmethod
    def get_material_by_id(cls, id):
        data = Database.find_one('study_materials', {'_id': id})
        return cls(**data)