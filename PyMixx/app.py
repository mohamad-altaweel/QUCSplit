# save this as app.py
from multiprocessing.connection import answer_challenge
from flask import Flask, session
from rest import RESTpresso
from logic import *
app = Flask(__name__)
rest = RESTpresso("root","0000","http://localhost:2480")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/Test')
def test():
    return "<p>Hello, World!</p>"

@app.route('/')
def hello():
    session['answers'] = list()
    firstQuestion = rest.getQuestion("YourProblemDomain")
    answers = rest.GetPossibleAnswers("YourProblemDomain")
    return {
        "question":firstQuestion,
        "answers":answers
    }

@app.route('/<given_question>/<answer>')
def traverse(given_question,answer):
    question = rest.getQuestion(given_question)
    newAnswer = (question["description"],answer)
    list = session['answers']
    AddNewAnswerToList(list,newAnswer)
    session['answers'] = list
    print(session['answers'])
    if question["type"] == "single":
        answer = answerSingleChoiceQuestion(question,answer)
        if answer["question"] == "Off":
            return {
                "answer":answer["answers"],
                "session":session["answers"]
            }
        else:
            return answer
    elif question["type"] == "text":
        answer = answerSingleChoiceQuestion(question,answer)
        if answer["question"] == "Off":
            return {
                "answer":answer["answers"],
                "session":session["answers"]
            }
        else:
            return answer
    elif question["type"] == "number":
        answer = answerNumberGivenQuestion(question,answer)
        if answer["question"] == "Off":
            return {
                "answer":answer["answers"],
                "session":session["answers"]
            }
        else:
            return answer
    else:
        return "<p>Not found!</p>"
