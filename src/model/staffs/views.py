from flask import Blueprint, request, session, render_template, url_for, make_response
from werkzeug.utils import redirect

from src.errors import UserErrors
from src.model.staffs.staff import Staff
from src.model.users.form import Form
from src.model.users.users import User

staffs_blueprint = Blueprint('staffs',__name__)

@staffs_blueprint.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        try:
            if Staff.is_login_valid(phone, password):
                session['phone'] = phone
                return redirect(url_for(".profile"))
            else:
                return render_template('staffs/login.html', error="Invalid phone or password")
        except UserErrors as e:
            return render_template('staffs/login.html', error=e.message)
    return render_template('staffs/login.html')


@staffs_blueprint.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        phone = request.form['phone']
        password = request.form['password']

        try:
            if Staff.register(name,phone,password):
                session['phone'] = phone
                return redirect(url_for(".profile"))
        except UserErrors as e:
            return render_template('staffs/register.html',error=e.message)

    return render_template('staffs/register.html')

@staffs_blueprint.route('profile')
def profile():
    if request.cookies.get('phone'):
        session['phone'] = request.cookies.get('phone')
    if session['phone'] is not None:
        response = make_response(render_template('staffs/profile.html', user=Staff.get_account(session['phone'])))
        response.set_cookie('phone',session['phone'])
        return response
    else:
        return render_template('home.html')

@staffs_blueprint.route('manage_students')
def manage_studetns():
    return render_template("staffs/manage_students.html")

@staffs_blueprint.route('register_student',methods=["GET","POST"])
def register_stuedent():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        course = request.form['course']
        status = request.form['status']
        try:
            User.register(name=name, phone=phone, course=course, status=status)
            return render_template("staffs/register_student.html", message="Registration Completed")
        except UserErrors as e:
            return render_template("staffs/register_student.html", message=e.message)


    return render_template("staffs/register_student.html")

@staffs_blueprint.route("student_status",methods=["GET","POST"])
def student_status():
    if request.method == "POST":
        try:
            phone = request.form['phone']
            student = User.get_account(phone)
            return render_template("staffs/edit_student.html",student=student)
        except UserErrors as e:
            return render_template("staffs/student_status.html", message = e.message)
    return render_template("staffs/student_status.html")

@staffs_blueprint.route('edit_student/<string:phone>',methods=["GET","POST"])
def edit_student(phone=None):
    if request.method == "POST":
        try:
            if phone is not None:
                status = request.form['status']
                User.update_status(phone,status)
                return render_template("staffs/edit_student.html",student=User.get_account(phone))
        except UserErrors as e:
            return render_template("staffs/student_status.html",message=e.message)

    return render_template("student_status.html",message="Nothing")

@staffs_blueprint.route('view_students',methods=["POST","GET"])
def view_students():
    if request.method == "POST":
        status = request.form['status']
        students = User.get_all({'status':status})
        return render_template("staffs/students.html",students=students)

    students = User.get_all()
    return render_template("staffs/students.html", students=students)




@staffs_blueprint.route('/logout')
def logout():
    session['phone'] = None
    return render_template('home.html')
