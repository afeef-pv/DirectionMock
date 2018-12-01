import pickle
from bson.binary import Binary
from src.common.database import Database
Database.initilize()


class Question(object):
    def __init__(self,question,options,answer):
        self.question = question
        self.options = options
        self.answer = answer

    def json(self):
        return {
            "question":self.question,
            "options":self.options,
            "answer":self.answer
        }

    def save_mongo(self):
        data = pickle.dumps(self.json())
        dic={"question_binary":Binary(data)}
        Database.insert("question",dic)


q = Question("who is afeef",['Software Engineer','Accountant','Euntrupuner','idiota'],'Software Engineer')
q.save_mongo()