from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms import quizCodeForm, answersForm, addSubjectForm, deleteQuestionForm
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_session import Session 
from datetime import timedelta
import secrets
import uuid
import random

#from databaseKark import DataBase          # MySQL      -> kark.no     -> Kun tilgjengelig ved bruk av VPN eller på UiTs wifi/internett (brukt for testing)
from dbPostgreSQL import DataBase         # PostgreSQL -> heroku.com  -> Ble brukt online


from questions import Question
from subjects import Subject
from answers import Answer
from user import User

SECRET_KEY = secrets.token_urlsafe(16)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY

# csrf = CSRFProtect(app)
# csrf.init_app(app)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours = 5)
app.config['SESSION_FILE_THRESHOLD'] = 100  
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


"################################################# LOGIN #################################################"


@login_manager.user_loader
def load_user(user_id):
    with DataBase() as db:
        user = User(*db.getUserById(user_id)[0])
    return user


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form['username']
        password = request.form['password']

        with DataBase() as db:
            usr = db.getUser(email)[0]
            if usr:
                current_user = User(*usr)
                if current_user.check_password(password):

                    if int(current_user.verified) == 1: #Må sjekkes med MySQL, men skal nå gå bra.
                        login_user(current_user, remember = True)

                        return redirect(url_for('teacher'))
                    else:
                        return render_template('login.html', usr = True, verified = False)
                
                else:
                    return render_template('login.html', usr = True, password = False)
            
            else:
                return render_template('login.html', usr = False)

    else:
        return render_template('login.html', usr = None)
    

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():

    with DataBase() as db:
        if request.method == "POST":

            req = request.form
            passwordHash = generate_password_hash(req['password'])

            username = req['e_mail']
            usr = db.getUser(username)
            uu_id = str(uuid.uuid4())

            if not usr:
                user = (
                    username,
                    passwordHash,
                    req['firstname'],
                    req['lastname'],
                    uu_id)

                db.createUser(user)

                return render_template('login.html')
            else:
                return render_template("signUp.html", usr = True)


        elif request.method == "GET":
            return render_template("signUp.html", username = None)




"################################################# BOTH #################################################"


@app.route("/home")
def home():
    return render_template('index.html')


"################################################# STUDENT #################################################"



@app.route("/") 
def quizCodePage():
    return render_template('quizCodePage.html')



@app.route("/quizCode", methods = ["POST"])
def quizCode():

    if request.method == "POST":

        form = quizCodeForm(request.form)
        session["quiz_code"] = form.quizCode.data

        return redirect( url_for('student') )



@app.route("/student")
def student():

    quiz_id = session["quiz_code"]

    try:   
        with DataBase() as db:
            question = Question(*db.getCurrentQuestion(quiz_id)[0][:-1])
            answer_id = db.getCurrentQuestion(quiz_id)[0][-1]
    except:
        question = ""
        answer_id = ""

    return render_template('student.html', question = question, quiz_id = quiz_id, answer_id = answer_id)


@app.route("/wait")
def wait():


    return render_template('wait.html')


@app.route("/addAnswer", methods = ["POST"])
def addAnswer():

    if request.method == "POST": 
        req = request.form
        form = answersForm(req)

        answer_id = form.answer_id.data
        answer = form.answer.data

        with DataBase() as db:
            db.addAnswer(answer_id, answer)
            
        if ("choice" in req) and req["choice"] != "Send inn":
            return redirect( url_for('student') )
        
    return redirect( url_for('wait') )





"################################################# TEACHER #################################################"


@app.route("/teacher", methods = ["GET", "POST"])
@login_required
def teacher():

    with DataBase() as db:
        while True:
            try:
                quiz_id = db.getQuizID(current_user.user_id)[0][0]
                break
            except:
                db.createQuizID(random.randint(999, 9999), current_user.user_id) #Rom for 9000 brukere akkurat nå i forhold til "ledige" quiz IDer.

        if request.method == "POST" and "set_current" in request.form:
            q_id = request.form["set_current"]
            db.resetCurrent(quiz_id)
            db.setCurrent(quiz_id, q_id)

        parent_id = request.args.get('parent_id')
        subject_id = request.args.get('subject_id')
        session["subject_id"] = subject_id

        if not subject_id:
            subjects = sorted([Subject(*i) for i in db.getSubjects(0)], key = lambda sub: sub.subject_name.lower())
            
            return render_template('subjects.html', quiz_id = quiz_id, subjects = subjects, subject_id = subject_id)
        

        elif parent_id == "0":
            subjects = sorted([Subject(*i) for i in db.getSubjects(subject_id)], key = lambda sub: sub.subject_name.lower())
            
            return render_template('subjects.html', quiz_id = quiz_id, subjects = subjects, subject_id = subject_id)


        elif parent_id != "0":
            try:
                currentQuestion = Question(*db.getCurrentQuestion(quiz_id)[0][:-1])
            except:
                currentQuestion = Question(0, "Ingen spørsmål valgt.", None, None, 0, 0)

            questions = [Question(*q) for q in db.getQuestionsBySubject(subject_id)]

            return render_template('questions.html', 
                                   quiz_id = quiz_id, 
                                   current = currentQuestion, questionLst = questions,  
                                   subject_id = subject_id)



@app.route('/addSubject', methods = ["POST"])
@login_required
def addSubject():

    if request.method == "POST":
        form = addSubjectForm(request.form)

        newSubject = form.subjectName.data
        subject_id = session["subject_id"]

        if not subject_id:
            subject_id = 0

        with DataBase() as db:
                db.createSubject(newSubject, subject_id)

    return redirect( url_for('teacher', parent_id = 0, subject_id = subject_id) )


#DELETE SUBJECT



@app.route('/add')
@login_required
def add():
    subject_id = session["subject_id"]

    return render_template('addQuestion.html', subject_id = subject_id)


@app.route('/tips')
@login_required
def tips():

    return render_template('tips.html')



@app.route('/addNew', methods = ["POST"])
@login_required
def addNew():

    subject_id = session["subject_id"]

    if request.method == "POST":
        req = request.form

        options1 = req["options1"]
        options2 = req["options2"]
        options3 = req["options3"]
        options4 = req["options4"]
        question = req["question"]
        subject = req["subject_id"]
        correctAnswer = int(req["correctAnswer"])

        with DataBase() as db:
            if options1 == "":
                db.addQuestion(question, subject, current_user.user_id)
            else:
                options_lst = [options1, options2, options3, options4]
                options = f'{options1},{options2},{options3},{options4}'
                db.addMultiQuestion(question, options, options_lst[correctAnswer], subject, current_user.user_id)

    return redirect( url_for('teacher', subject_id = subject_id) )



@app.route('/deleteQuestion', methods = ["POST"])
@login_required
def deleteQuestion():

    subject_id = session["subject_id"]

    if request.method == "POST":
        form = deleteQuestionForm(request.form)

        question_id = form.question_id.data

        with DataBase() as db:
            db.deleteQuestionById(question_id)

    return redirect( url_for('teacher', subject_id = subject_id) )



@app.route("/answers")
@login_required
def answers():

    with DataBase() as db:
        quiz_id = db.getQuizID(current_user.user_id)[0][0] 
        question = Question(*db.getCurrentQuestion(quiz_id)[0][:-1])
        quiz_id = db.getQuizID(current_user.user_id)[0][0]

        try:
            answerLst = [Answer(*a) for a in db.getAnswers(quiz_id)]
        except:
            answerLst = []

        counts = [0, 0, 0, 0]
        if question.options != None:
            options = question.options

            for i in range(len(options)):
                for a in answerLst:
                    if a.answer == options[i]:
                        counts[i] += 1

            

    return render_template("answerTable.html", quiz_id = quiz_id, answers = answerLst, current = question, counts = counts)


@app.route("/quit")
@login_required
def quitSession():

    with DataBase() as db:
        quiz_id = db.getQuizID(current_user.user_id)[0][0] 

        db.resetCurrent(quiz_id)
        quizSet = {x[0] for x in db.getAnswersById(quiz_id)}

        for answer_id in quizSet:
            db.deleteAnswers(answer_id)

    return redirect( url_for('quizCodePage') )



if __name__ == '__main__':
    app.run()