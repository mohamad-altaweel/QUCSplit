import requests

username = "root"
password = "0000"
root_url = "http://localhost:2480"

class RESTpresso():

    def __init__(self, username, password, root_url) -> None:
        self.username = username
        self.password = password
        self.root_url = root_url

    def QuestionExists(self,NodeName):
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

    def GetPossibleAnswers(self,Question):
        list_of_answers = []
        if self.QuestionExists(Question):
            response = requests.get("{}/function/questionDB/GetPossibleAnswers/{}".format(root_url,Question), auth = (username,password))
            if response.status_code == 200:
                for answer in response.json()["result"]:
                    list_of_answers.append(answer)
            else:
                print("Error -- Response code {}".format(response.status_code))
        else:
            print("Question does not Exist")
        return list_of_answers


    def AnswerExists(self, Answer):
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

    def AnswerAssignedToTheQuestion(self, Question, Answer):
        assigned = False
        if self.AnswerExists(Answer) and self.QuestionExists(Question):
            if Answer in self.GetPossibleAnswers(Question):
                assigned = True
        else:
            print("Answer or Question not found")
        return assigned

    def CreateQuestion(self, Question):
        response = requests.post("{}/function/questionDB/CreateQuestion/{}".format(root_url,Question), auth = (username,password))
        if response.status_code == 200:
            return response.json()["@rid"]
        else:
            print("Error -- Status code: {}".format(response.status_code))

    def AssignAnswer(self, Answer, In, Out):
        response = requests.post("{}/function/questionDB/assignAnswer/{}/{}/{}".format(root_url,Answer,In,Out), auth = (username,password))
        if response.status_code == 200:
            return response.json()["@rid"]
        else:
            print("Error -- Status code: {}".format(response.status_code))

    def testConnection(self):
        response = requests.get("{}/function/questionDB/testConnection".format(root_url), auth = (username,password))
        if response.status_code == 200: 
            print("Connection success")
            return True
        else:
            print("Error -- Status code: {}".format(response.status_code))
            return False
    
    def getQuestion(self,NodeName):
        question = None
        response = requests.get("{}/function/questionDB/QuestionExists/{}".format(root_url,NodeName), auth = (username,password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                print("Question exists")
                exists = response.json()["result"][0]
            else:
                print("Question does not exist")
        else:
            print("Error -- Status Code {}".format(response.status_code))
        return exists

    def getNextNode(self,EdgeId):
        question = None
        response = requests.get("{}/function/questionDB/GetNextNode/{}".format(root_url,EdgeId), auth = (username,password))
        if response.status_code == 200:
            print(response.json())
            if len(response.json()["result"]) > 0:
                print("Question exists")
                question = response.json()["result"][0]
            else:
                print("Question does not exist")
        else:
            print("Error -- Status Code {}".format(response.status_code))
        return question