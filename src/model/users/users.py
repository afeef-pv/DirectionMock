from flask import session

from src.common.database import Database
from src.model.users.form import Form
from src.model.exams.tests import Test
import src.errors as UserErrors


class User(object):



    @staticmethod
    def get_by_phone(phone):
        return Form.get_form(phone)

    @staticmethod
    def get_account(phone):
        user = Form.get_form(phone)
        if user is not None:
            return user
        else:
            raise UserErrors.UserNotExistError("Student by this number is not found")

    @classmethod
    def register(cls,name,phone,course,status):
        if cls.get_by_phone(phone) is None:
            user = Form(name=name,phone=phone,course=course,status=status)
            user.save_to_mongo()
            return True
        else:
            raise UserErrors.UserAlreadyExistError("User in this phone No already Exist")

    @classmethod
    def login(cls,phone):
        if len(phone) < 10:
            raise UserErrors.InvalidPhoneError("Please Enter A valid Phone Number")
        return cls.get_by_phone(phone)


    @staticmethod
    def logout():
        session['phone'] = None

    @staticmethod
    def get_tests(course):
        tests = Database.find_all('tests',{'course':course,'status':'active'})
        print(tests)
        return tests

    @staticmethod
    def add_test():
        test = Test("Daily Test","DAILY")
        test.save_to_mongo()

    @classmethod
    def update_status(cls,phone,status):
        if cls.get_by_phone(phone) is not None:
            Database.update('students',{'phone':phone},{'$set':{'status':status}})
        else:
            raise UserErrors.UserNotExistError("User Not Exists")

    @staticmethod
    def get_all(query={}):
        return Database.find_all('students',query)


