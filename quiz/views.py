from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import *
from .app import db



@app.route('/quiz/api/v1.0/questionnaires', methods=['GET'])
def get_tasks():
    questionnaires = get_allquestionnaires()
    return questionnaires

@app.route('/quiz/api/v1.0/questionnaires', methods=['POST'])
def create_questionnaire():
    if not request.json or not 'name' in request.json :
        abort(400)
    questionnaire = Questionnaire(name=request.json['name'], uri=request.json['uri'])
    db.session.add(questionnaire)
    db.session.commit()
    return jsonify({'questionnaire': questionnaire.to_json()}), 201


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['GET'])
def get_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    return jsonify({'questionnaire': questionnaire.to_json()})


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/questions', methods=['POST'])
def create_question(questionnaire_id):
    if not request.json or not 'title' in request.json:
        abort(400)
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    question = Question(
        title=request.json['title'],
        questionType="text",
        questionnaire_id=questionnaire_id
        
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'question': question.to_json()}), 201


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/questions', methods=['GET'])
def get_questions(questionnaire_id):
    return get_allquestions(questionnaire_id)


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/questions/<int:question_id>', methods=['GET'])
def get_question(questionnaire_id, question_id):
    return get_onequestion(questionnaire_id,question_id)


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/questions/<int:question_id>', methods=['PUT'])
def modif_question(questionnaire_id, question_id):
    question = Question.query.filter_by(id=question_id, questionnaire_id=questionnaire_id).first()
    if question is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'questionType' in request.json and type(request.json['questionType']) != str:
        abort(400)
    question.title = request.json.get('title', question.title)
    question.questionType = request.json.get('questionType', question.questionType)
    db.session.commit()
    return jsonify({'question': question.to_json()})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/questions/<int:question_id>', methods=['DELETE'])
def delete_question(questionnaire_id, question_id):
    question = Question.query.filter_by(id=question_id, questionnaire_id=questionnaire_id).first()
    if question is None:
        abort(404)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'result': True})



@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['DELETE'])
def delete_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['PUT'])
def modifier_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    questionnaire.name = request.json.get('name', questionnaire.name)
    db.session.commit()
    return jsonify({'questionnaire': questionnaire.to_json()})







