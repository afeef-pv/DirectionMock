from flask import Blueprint, session, render_template

from src.model.results.result import Result

results_blueprint = Blueprint("results",__name__)

@results_blueprint.route('student_results')
def studetn_result():
    results = Result.get_results_phone(session['phone'])
    return render_template('/users/results.html',results = results)
