import uuid

from flask import session
import src.errors as UserErrors

from src.common.database import Database


class Staff(object):
    def __init__(self,name,phone,password,_id = None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.name=name
        self.phone=phone
        self.password=password


    @classmethod
    def get_account(cls,phone):
        staff =Database.find_one('staffs',{'phone':phone})
        if staff is None:
            return None
        else:
            return cls(**staff)

    def json(self):
        return {
            "_id":self._id,
            "name":self.name,
            "phone":self.phone,
            "password":self.password
        }

    def save_to_mango(self):
            Database.insert("staffs",self.json())

    @classmethod
    def register(cls,name,phone,password):
        if cls.get_account(phone) is None:
            staff = cls(name,phone,password)
            staff.save_to_mango()
            session['phone'] = phone
            return True
        else:
            raise UserErrors.UserAlreadyExistError("User Already Exist")

    @classmethod
    def login(cls,phone):
        session['phone'] = phone

    @classmethod
    def is_login_valid(cls,phone,password):
        staff = cls.get_account(phone)
        if staff is None:
            raise UserErrors.UserNotExistError("Account does not exist")
        return staff.password == password


    @classmethod
    def logout(cls):
        session['phone'] = None

    @staticmethod
    def get_tests():
        tests = Database.find_all('tests', {'status': 'active'})
        print(tests)
        return tests
