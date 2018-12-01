from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.errors import UserErrors
from src.model.users.users import User

user_blueprint = Blueprint('users',__name__)

@user_blueprint.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        try:
            user = User.login(phone)
            if user is not None and user.status == "joined":
                session['phone'] = phone
                return redirect(url_for(".profile"))
            else:
                return render_template('users/login.html',error="No account found in this number")
        except UserErrors as e:
            return render_template('users/login.html',error=e.message)

    return render_template('users/login.html')

@user_blueprint.route('profile')
def profile():
    if session['phone'] is not None:
        return render_template('users/profile.html', user=User.get_by_phone(session['phone']))
    else:
        return render_template('home.html')

@user_blueprint.route('logout')
def logout():
    session['phone'] = None
    return render_template('home.html')