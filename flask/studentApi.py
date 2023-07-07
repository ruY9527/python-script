from flask import Blueprint,render_template, request

student_api = Blueprint('student_api', __name__)


@student_api.route('/student')
def student():
    return render_template('student.html')

@student_api.route('/student/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html",result = result)