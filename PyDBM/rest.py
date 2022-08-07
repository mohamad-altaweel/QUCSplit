from genericpath import exists
import requests
import json

from sklearn.multiclass import OutputCodeClassifier

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
    list_of_answers = []
    if QuestionExists(Question):
        response = requests.get("{}/function/questionDB/GetPossibleAnswers/{}".format(root_url,Question), auth = (username,password))
        if response.status_code == 200:
            for answer in response.json():
                list_of_answers.append(answer)
        else:
            print("Error -- Response code {}".format(response.status_code))
    else:
        print("Question does not Exist")


def AnswerExists(Answer):
    exists = False
    response = requests.get("{}/function/questionDB/AnswerExists/{}".format(root_url,Answer), auth = (username,password))
    if response.status_code == 200:
        if len(response.json()["result"]) > 0:
            print("Answer exists")
            exists = True
        else:
            print("Answer does not exist")
    else:
        print("Error -- Status Code {}".format(response.status_code))
    return exists

def AnswerAssignedToTheQuestion(Question, Answer):
    assigned = False
    if AnswerExists(Answer) and QuestionExists(Question):
        if Answer in GetPossibleAnswers(Question):
            assigned = True
    else:
        print("Answer or Question not found")
    return assigned

def CreateQuestion(Question):
    response = requests.post("{}/function/questionDB/CreateQuestion/{}".format(root_url,Question), auth = (username,password))
    if response.status_code == 200:
        return response.json()["@rid"]
    else:
        print("Error -- Status code: {}".format(response.status_code))

def AssignAnswer(Answer, In, Out):
    response = requests.post("{}/function/questionDB/assignAnswer/{}/{}/{}".format(root_url,Answer,In,Out), auth = (username,password))
    if response.status_code == 200:
        return response.json()["@rid"]
    else:
        print("Error -- Status code: {}".format(response.status_code))