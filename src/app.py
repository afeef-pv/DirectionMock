from flask import Flask, render_template, session

'''from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey('server.key')
context.use_certificate('server.crt')'''

from src.common.database import Database
from src.model.users.users import User

app = Flask(__name__)
app.config.from_object('config')
app.secret_key='8mkrkgbhkt'

from src.model.users.views import user_blueprint
from src.model.staffs.views import staffs_blueprint
from src.model.exams.views import exams_blueprint
from src.model.study_materials.views import materials_blueprint
from src.model.results.views import results_blueprint

app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(staffs_blueprint,url_prefix='/staffs')
app.register_blueprint(exams_blueprint,url_prefix='/exams')
app.register_blueprint(materials_blueprint,url_prefix='/study_materials')
app.register_blueprint(results_blueprint,url_prefix='/results')

@app.before_first_request
def init_db():
    Database.initilize()

@app.route('/')
def home_default():
        return render_template('home.html')

@app.route('/home')
def home():
    if session['phone'] is None:
        return render_template('home.html')
    else:
        return render_template('users/profile.html',user=User.get_by_phone(session['phone']))