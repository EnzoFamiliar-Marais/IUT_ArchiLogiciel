from .app import app, db

@app.cli.command('initdb')
#@click.argument('filename')
def syncbd():
    '''Creates the tables and populates them with data.'''
    # création de toutes les tables
    db.create_all()
    # chargement de notre jeu de données
    # import yaml
    # data = yaml.load(open(filename), Loader=yaml.FullLoader)
    # # import des modèles
    # from .models import Question, Questionnaire
    # # création des questionnaires et des questions
    # for questionnaire_data in data:
    #     questionnaire = Questionnaire(name=questionnaire_data['name'])
    #     db.session.add(questionnaire)
    #     db.session.commit()
    #     for question_data in questionnaire_data['questions']:
    #         question = Question(
    #             title=question_data['title'],
    #             questionType=question_data['questionType'],
    #             questionnaire_id=questionnaire.id
    #         )
    #         db.session.add(question)
    # db.session.commit()