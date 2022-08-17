# save this as app.py
from multiprocessing.connection import answer_challenge
from flask import Flask, request
from markupsafe import escape
from rest import RESTpresso
app = Flask(__name__)
rest = RESTpresso("root","0000","http://localhost:2480")


@app.route('/Test')
def test():
    return "<p>Hello, World!</p>"

@app.route('/')
def hello():
    firstQuestion = rest.getQuestion("YourProblemDomain")
    answers = rest.GetPossibleAnswers("YourProblemDomain")
    return {
        "question":firstQuestion,
        "answers":answers
    }

@app.route('/<question>/<answer>')
def traverse(question,answer):
    firstQuestion = rest.getQuestion(question)
    answers = rest.GetPossibleAnswers(question)
    for possible in answers:
            if possible["name"] == answer:
                print(possible["@rid"])
                node = rest.getNextNode(possible["@rid"][1:])
                print(node)
                NextQuestion = node["name"]
                Nextanswers = rest.GetPossibleAnswers(NextQuestion)
                return {
                    "question":NextQuestion,
                    "answers":Nextanswers
            }