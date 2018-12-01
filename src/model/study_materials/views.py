from flask import Blueprint, render_template, request

from src.model.study_materials.materials import Material

materials_blueprint = Blueprint('study_materials',__name__)


@materials_blueprint.route('organise_materials')
def organise_materials():
    #For staffs
    return render_template('/study_materials/organise_materials.html')


@materials_blueprint.route('create_material',methods=['POST','GET'])
def create_material():
    #For staffs
    if request.method == 'POST':
        subject=request.form['subject']
        course=request.form['course']
        content = request.form['content']
        material = Material(subject,course,content)
        material.save_to_mongo()
        return render_template('/study_materials/view_material.html',material=material)
    return render_template('/study_materials/create_material.html')


@materials_blueprint.route('view_materials')
def view_materials():
    materials = Material.get_materials()
    return render_template('/study_materials/view_materials.html',materials=materials)


@materials_blueprint.route('view_material/<string:id>')
def view_material(id):
    #need to code secure access
    material = Material.get_material_by_id(id)
    return render_template('/study_materials/view_material.html',material=material)


@materials_blueprint.route('view_materials/<string:course>')
def view_materials_student(course):
    materials = Material.get_materials_by_course(course)
    return render_template('/study_materials/student/view_materials.html',materials=materials)


@materials_blueprint.route('student/view_material/<string:id>')
def view_material_student(id):
    #need to code secure access
    material = Material.get_material_by_id(id)
    return render_template('/study_materials/student/view_material.html',material=material)