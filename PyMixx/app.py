# save this as app.py
from genericpath import exists
from flask import Flask, session, redirect, url_for, request
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
    newAnswer = (question["description"],answer,question["name"])
    if "answers" not in session:
        session['answers'] = list()
    list = session['answers']
    AddNewAnswerToList(list,newAnswer)
    session['answers'] = list
    if question["type"] == "single":
        answer = answerSingleChoiceQuestion(question,answer)
        if answer["question"] == "Off":
            return {
                "answer":answer["answers"],
                "session":session["answers"][:1]
            }
        elif answer["question"] == "Dead":
            # trigger similarity function
            return "<p>You reached a dead End here..!</p>"
        else:
            return answer
    elif question["type"] == "text":
        answer = answerSingleChoiceQuestion(question,answer)
        if answer["question"] == "Off":
            return {
                "answer":answer["answers"],
                "session":session["answers"]
            }
        elif answer["question"] == "Dead":
            # trigger similarity function
            return "<p>You reached a dead End here..!</p>"
        else:
            return answer
    elif question["type"] == "number":
        answer = answerNumberGivenQuestion(question,answer)
        if answer["question"] == "Off":
            return {
                "answer":answer["answers"],
                "session":session["answers"]
            }
        elif answer["question"] == "Dead":
            # trigger similarity function
            return "<p>You reached a dead End here..!</p>"
        else:
            return answer
    else:
        return "<p>Not found!</p>"


@app.route('/back')
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

@app.route('/OneTextAnswer')
def AnswerFullText():
    data = request.get_json()
    text = data["text"]
    #trigger similarity function
    return {
        "question":"We have not implemented this function!Coming soon"
    }

@app.route('/ListInfo')
def AnswerListInfo():
    response = {"question":"Off","answers":"Unknown"}
    data = request.get_json()
    answers = data["answers"]
    copy_of_answers = answers.copy()
    for i in answers:
        for key in i:
            if rest.QuestionExists(key):
                possibleEdges = rest.GetPossibleAnswers(key)
                if len(possibleEdges) == 0:
                    break
                else:
                    next = getAnswerFromName(possibleEdges,i[key])
                    if next is not None:
                        copy_of_answers.remove(i)
                        nextNode = rest.getNextNode(next["@rid"][1:])
                        if nextNode["@class"] == "decision":
                            response["answers"] = nextNode["name"]
            else:
                break
    if len(copy_of_answers) > 0:
        print("I am not finished")
    return response