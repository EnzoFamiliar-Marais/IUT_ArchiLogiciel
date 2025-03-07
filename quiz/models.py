from flask import url_for
from .app import db

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


    def __init__(self, name, uri):
        self.name = name

    def __repr__(self):
        return "<Questionnaire (%d) %s>" % (self.id, self.name)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'uri': url_for('get_questionnaire', questionnaire_id=self.id, _external=True)
        }
        return json


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    questionType = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship("Questionnaire", backref=db.backref("questions", lazy="dynamic"))

    def __init__(self, title, questionType, questionnaire_id):
        self.title = title
        self.questionType = questionType
        self.questionnaire_id = questionnaire_id

    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'questionType': self.questionType,
            'questionnaire_id': self.questionnaire_id
        }
        return json


def get_allquestionnaires():
    questionnaires = Questionnaire.query.all()
    return [q.to_json() for q in questionnaires]

def get_allquestions(questionnaire_id):
    questions = Question.query.filter_by(questionnaire_id=questionnaire_id).all()
    return [q.to_json() for q in questions]

def get_onequestion(questionnaire_id, question_id):
    question = Question.query.filter_by(id=question_id, questionnaire_id=questionnaire_id).first()
    if question:
        return question.to_json()
    else:
        return "ca marche pas y'a pas de question"
