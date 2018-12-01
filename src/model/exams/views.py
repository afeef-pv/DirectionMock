import datetime

from flask import Blueprint, request, render_template, session

from src.model.exams.question import Question
from src.model.exams.question_paper import Questions
from src.model.exams.tests import Test
from src.model.results.result import Result

exams_blueprint = Blueprint("exams",__name__)

questions = []

@exams_blueprint.route('organise_tests')
def organise_tests():
    """
    organise available tests under specified course
    :return:
    """
    tests = Test.get_tests()
    if tests is None:
        tests = []
    return render_template('staffs/exams/organise_tests.html', tests=tests)

@exams_blueprint.route('/create_test',methods=['GET','POST'])
def create_test():
    """
    create test
    :return:
    """
    if request.method == "POST":
        name = request.form['tname']
        course = request.form['course']
        test = Test(test_name=name, course=course)
        test.save_to_mongo()
        tests = Test.get_tests()
        if tests is None:
            tests = []
        return render_template('staffs/exams/organise_tests.html', tests=tests)

    return render_template('staffs/exams/create_test.html')

@exams_blueprint.route('/organise_questions/<string:id>')
def organise_questions(id):
    """

    :param id: Organise questions under a perticular test
    :return:
    """
    papers = Questions.get_all_questions_by_test_id(id)
    test=Test.get_test_by_id(id)
    return render_template('staffs/exams/organise_questions.html',papers=papers,test=test)

@exams_blueprint.route('/add_question/<string:test_id>',methods=['POST','GET'])
def add_question(test_id):
    """

    :param test_id: id of test in which questions are being added
    :return: create question page
    """
    if request.method == 'POST':
        global questions
        question = request.form['question']
        options = [request.form['a'], request.form['b'], request.form['c'], request.form['d']]
        answer = request.form['answer']
        questions.append(Question(question, options, answer))
        test = Test.get_test_by_id(test_id)
        return render_template('staffs/exams/create_questions.html', test=test)

    test = Test.get_test_by_id(test_id)
    return render_template('staffs/exams/create_questions.html', test=test)

@exams_blueprint.route('/create_question/<string:test_id>',methods=['POST'])
def create_question(test_id):
    """

    :param test_id: id of the test
    :return: create a question set under the given test id
    """
    global questions
    test=Test.get_test_by_id(test_id)
    subject = request.form['subject']
    paper = Questions(test.course,subject,test_id,questions)
    paper.save_to_mongo()
    questions =[]
    return render_template('staffs/exams/create_questions.html',test=test)

@exams_blueprint.route('/view_questions/<string:id>')
def view_questions(id):
    """

    :param id: exam id
    :return:Question paper
    """
    paper = Questions.get_questions_by_id(id)
    return render_template('staffs/exams/view_questions.html',paper=paper)
'''
    Student sections below
'''
@exams_blueprint.route('tests/<string:course>')
def tests(course):
    tests = Test.get_test_by_course(course)
    if tests == None:
        tests = []
    return render_template('users/exams/tests.html',tests=tests)

@exams_blueprint.route('exams/<string:course>')
def exams(course):
    papers = Questions.get_questions(course)
    return render_template('users/exams/exams.html', papers=papers)

@exams_blueprint.route('/get_exam/<string:id>')
def get_exam(id):
    paper=Questions.get_questions_by_id(id)
    return render_template('users/exams/exam.html',paper=paper)

@exams_blueprint.route('/submit_exam/<string:id>',methods=["POST"])
def submit_exam(id):
    paper=Questions.get_questions_by_id(id)
    mark = 0
    for q in paper.questions:
        if request.form[q.question] == q.answer:
            mark+=5
    result = Result(session['phone'],paper.subject, paper.test_id, mark,datetime.datetime.now())
    result.save_to_mongo()
    return render_template("users/exams/result.html",mark=mark)