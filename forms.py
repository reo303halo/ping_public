from wtforms import Form, StringField
from wtforms.validators import Length, InputRequired
from wtforms.fields import HiddenField
from flask_wtf import FlaskForm

class quizCodeForm(Form):
    quizCode = StringField("quizCode", validators=[InputRequired(), Length(max=4)])


class answersForm(Form):
    answer_id = HiddenField("answer_id", validators=[InputRequired(), Length(max=5)])
    answer = StringField("answer", validators=[InputRequired(), Length(max=500)])


class addSubjectForm(Form):
    subjectName = StringField("subjectName", validators=[InputRequired(), Length(max=50)])


class deleteQuestionForm(Form):
    question_id = HiddenField("question_id", validators=[InputRequired(), Length(max=5)])
