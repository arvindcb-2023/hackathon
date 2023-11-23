from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import re
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['devfest']
login = db['login']
papers = db['papers']
projects = db['projects']
student = db['student']

DB = client.devfest
Collection = DB.professor
login_student='Catheline'
login_professor='Kaira'
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        login = db.login
        login_result = list(login.find({"userName":username, "password":password}))
        if len(login_result)==1:
            if login_result[0]['role']=='professor':
                login_professor=login_result[0]['Name']
                return(redirect(url_for('professor', profname=login_professor)))
                #professor()
                #return
            elif login_result[0]['role']=='student':
                login_student=login_result[0]['Name']
                return(redirect(url_for('student', stuname=login_student)))
                #student()
                #return
    return render_template('index.html')

@app.route('/student')
def student():
        Projects = list(projects.find({}))
        Student = list(db.student.find({}))
        Professor = list(db.professor.find({}))
        return render_template('student.html', projects=Projects, student=Student, professor=Professor, stuname=login_student)

@app.route('/professor')
def professor():
        Projects = list(projects.find({}))
        Student = list(db.student.find({'name': 'Catheline'}))
        Professor = list(db.professor.find({}))
        Papers = list(db.papers.find({}))
        return render_template('professor.html', projects=Projects, student=Student, professor=Professor, profname=login_professor, papers=Papers)

@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'POST':
        user_data = request.form['user_data']
        print(f"Received data from the form: {user_data}")
        pattern = f"{user_data}.*"
        result1 = list(Collection.find({'name':{ '$regex': pattern, "$options":"i"}}))
        result2 = list(Collection.find({'keyword':{ '$regex': pattern, "$options":"i"}}))
        return render_template('results.html', resultset1=result1, resultset2=result2)

@app.route('/logout')
def logout():
    #Session destroy code to be added after session has been created
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)