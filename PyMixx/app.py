# save this as app.py
from flask import Flask, session, redirect, url_for, request
from logic import *
from nlp import RefCaseComparator
import logging
from flask import has_request_context, request
import argparse
import json
from flask_cors import CORS, cross_origin
from flask_session import Session


def create_app(config=None):
        # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    if config is not None:
        app.config.from_file(config,load=json.load)
    else:
        raise FileNotFoundError()
    

    refCaseCompare = RefCaseComparator()
    refCaseCompare.BuildKeywordsVectorsForEachDocument(app.config["REF_FILES"])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Main logger")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('info.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    backbone = Backbone(app.config["USERNAME"],app.config["PASSWORD"],app.config["ROOT_URL"],app.config["DATABASE"],logger)

    @app.route('/Test')
    def test():
        return "<p>Hello, World!</p>"

    @app.route('/')
    @cross_origin(supports_credentials=True)
    def hello():
        session['answers'] = list()
        firstQuestion = backbone.getFirstQuestion()
        return {"header":"question","context":firstQuestion}

    @app.route('/<given_question>/<answer>')
    @cross_origin(supports_credentials=True)
    def traverse(given_question,answer):
        if answer != "noIdea":
            question = backbone.getQuestion(given_question)
            if "description" in question:
                newAnswer = (question["description"],answer,question["name"])
            else:
                newAnswer = (question["name"],answer,question["name"])
            if "answers" not in session:
                session['answers'] = list()
            list_of_answers = session['answers']
            print(list_of_answers)
            backbone.AddNewAnswerToList(list_of_answers,newAnswer)
            session['answers'] = list_of_answers
            if question["type"] == "single":
                answer = backbone.answerSingleChoiceQuestion(question,answer)
                if answer["question"] == "Off":
                    return {"header":"decision","context":{ "answer":answer["answers"],"session":session["answers"]}}
                elif answer["question"] == "Dead":
                    return redirect(url_for('traverse',given_question =given_question , answer ="noIdea"))
                else:
                    return {"header":"question","context":answer}
            elif question["type"] == "text":
                answer = backbone.answerSingleChoiceQuestion(question,answer)
                if answer["question"] == "Off":
                    return {"header":"decision","context":{ "answer":answer["answers"],"session":session["answers"]}}
                elif answer["question"] == "Dead":
                    return redirect(url_for('traverse',given_question =given_question , answer ="noIdea"))
                else:
                    return {"header":"question","context":answer}
            elif question["type"] == "number":
                answer = backbone.answerNumberGivenQuestion(question,answer)
                if answer["question"] == "Off":
                    return {"header":"decision","context":{ "answer":answer["answers"],"session":session["answers"]}}
                elif answer["question"] == "Dead":
                    return redirect(url_for('traverse',given_question =given_question , answer ="noIdea"))
                else:
                    return {"header":"question","context":answer}
            else:
                return {"header":"NotFound"}
        else:
            return {"header":"traversed","context":{"answer":"You have the following possiblites","session":backbone.getAllpossible(given_question)}}


    @app.route('/back')
    @cross_origin(supports_credentials=True)
    def go_back():
        list = session['answers']
        if len(list) > 0:
            list.pop()
        session['answers'] = list
        if len(session['answers']) == 0:
            return redirect(url_for('hello'))
        else:
            last_question = session['answers'][-1]
            return redirect(url_for('traverse',given_question =last_question[2] , answer =last_question[1]))

    @app.route('/OneTextAnswer', methods = ['POST', 'GET'])
    def AnswerFullText():
        data = request.json
        text = data["text"]
        similar = refCaseCompare.getSimilarCase(text)
        return {
            "question":"Your case is very similar to this one",
            "case":similar[1],
            "accuracy":similar[0] * 100,
            "problem context exactness":similar[2]
        }

    @app.route('/ListInfo')
    def AnswerListInfo():
        remoteAddress = request.remote_addr if has_request_context() else "Unknown"
        response = {"header":"decision","question":"Off","answers":"Unknown"}
        data = request.get_json()
        answers = data["answers"]
        copy_of_answers = answers.copy()
        for i in answers:
            for key in i:
                if backbone.quesionExists(key):
                    possibleEdges = backbone.getAllpossibleAnswers(key)
                    if len(possibleEdges) == 0:
                        break
                    else:
                        next = backbone.getAnswerFromName(possibleEdges,i[key])
                        if next is not None:
                            copy_of_answers.remove(i)
                            nextNode = backbone.getNextNode(next["@rid"][1:])
                            if nextNode["@class"] == "decision":
                                response["answers"] = nextNode["name"]
                else:
                    break
        if len(copy_of_answers) > 0:
            logger.warning("{} : I am not finished".format(remoteAddress))
        return response

    return app




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcoem to PyMixx app')
    parser.add_argument('config', type=str,help='A required path for config.json file')
    args = parser.parse_args()
    app = create_app(args.config)
    app.run()