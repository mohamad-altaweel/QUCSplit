from turtle import pos

from sympy import false
from rest import RESTpresso
rest = RESTpresso("root","0000","http://localhost:2480")


def answerSingleChoiceQuestion(question,answer):
    answers = rest.GetPossibleAnswers(question["name"])
    possible = getAnswerFromName(answers,answer)
    node = rest.getNextNode(possible["@rid"][1:])
    Nextanswers = rest.GetPossibleAnswers(node["name"])
    print(node["@class"])
    if node["@class"] == "decision":
        return {
            "question":"Off",
            "answers": node["name"]
        }
    elif len(Nextanswers) == 0 and node["@class"] is not "decision" :
        return {
            "question":"Dead",
            "answers": []
        }
    else:
        return {
                    "question":node,
                    "answers":Nextanswers
        }

def answerNumberGivenQuestion(question,answer):
    answers = rest.GetPossibleAnswers(question["name"])
    Node = None
    if int(answer) > int(question["decision"]):
        Node = getAnswerFromName(answers, "MoreThan{}".format(int(question["decision"])))
    else:
        Node = getAnswerFromName(answers, "LessThan{}".format(int(question["decision"])))
    nextNode = rest.getNextNode(Node["@rid"][1:])
    Nextanswers = rest.GetPossibleAnswers(Node["name"])
    if nextNode["@class"] == "decision":
        return {
            "question":"Off",
            "answers": nextNode["name"]
        }
    elif len(Nextanswers) == 0 and nextNode["@class"] is not "decision" :
        return {
            "question":"Dead",
            "answers": []
        }
    else:
        return {
                    "question":nextNode,
                    "answers":Nextanswers
        }
    
def getAnswerFromName(answers,name):
    for possible in answers:
        if possible["name"] == name:
            return possible
        else:
            pass

def AddNewAnswerToList(list,newAnswer):
    isNew = True
    for i in range(len(list)):
        if newAnswer[0] == list[i][0]:
            list[i] = newAnswer
            isNew = False
    if isNew:
        list.append(newAnswer)
