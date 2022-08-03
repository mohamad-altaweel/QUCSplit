from genericpath import exists
import requests
import json

username = "root"
password = "0000"
root_url = "http://localhost:2480"

def QuestionExists(NodeName):
    exists = False
    response = requests.get("{}/function/questionDB/QuestionExists/{}".format(root_url,NodeName), auth = (username,password))
    if response.status_code == 200:
        if len(response.json()["result"]) > 0:
            print("Question exists")
            exists = True
        else:
            print("Question does not exist")
    else:
        print("Error -- Status Code {}".format(response.status_code))
    return exists

def GetPossibleAnswers(Question):
    pass

def AnswerExists(Answer):
    pass

def AnswerAssignedToTheQuestion(Question, Answer):
    pass

def CreateQuestion(Question):
    pass

def AssignAnswers(AnswersList, Question):
    pass