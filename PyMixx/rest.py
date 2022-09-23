import requests
import logging
"""
Communicates with database through REST API to reterive different information
@required : username, password for authenication, database name, and RootURL where is the database deployed (locally : http://localhost:XXXX)
"""
class RESTpresso():

    def __init__(self, username, password, root_url, database,logger) -> None:
        self.username = username
        self.password = password
        self.root_url = root_url
        self.database = database
        self.logger = logger

    def QuestionExists(self,NodeName):
        exists = False
        response = requests.get("{}/function/{}/QuestionExists/{}".format(self.root_url,self.database,NodeName), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                self.logger.info("Question exists")
                exists = True
            else:
                self.logger.warning("Question does not exist")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return exists

    def GetPossibleAnswers(self,Question):
        list_of_answers = []
        if self.QuestionExists(Question):
            response = requests.get("{}/function/{}/GetPossibleAnswers/{}".format(self.root_url,self.database,Question), auth = (self.username,self.password))
            if response.status_code == 200:
                for answer in response.json()["result"]:
                    list_of_answers.append(answer)
            else:
                self.logger.error("Error -- Response code {}".format(response.status_code))
        return list_of_answers


    def AnswerExists(self, Answer):
        exists = False
        response = requests.get("{}/function/{}/AnswerExists/{}".format(self.root_url,self.database,Answer), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                self.logger.info("Answer exists")
                exists = True
            else:
                self.logger.warning("Answer does not exist")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return exists

    def AnswerAssignedToTheQuestion(self, Question, Answer):
        assigned = False
        if self.AnswerExists(Answer) and self.QuestionExists(Question):
            if Answer in self.GetPossibleAnswers(Question):
                assigned = True
        else:
            self.logger.warning("Answer or Question not found")
        return assigned

    def testConnection(self):
        response = requests.get("{}/function/{}/testConnection".format(self.root_url,self.database), auth = (self.username,self.password))
        if response.status_code == 200: 
            self.logger.info("Connection success")
            return True
        else:
            self.logger.error("Error -- Status code: {}".format(response.status_code))
            return False
    
    def getQuestion(self,NodeName):
        question = None
        response = requests.get("{}/function/{}/QuestionExists/{}".format(self.root_url,self.database,NodeName), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                self.logger.info("Question exists")
                question = response.json()["result"][0]
            else:
                self.logger.warning("Question does not exist")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return question

    def getNextNode(self,EdgeId):
        question = None
        response = requests.get("{}/function/{}/GetNextNode/{}".format(self.root_url,self.database,EdgeId), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                self.logger.info("Next Node exists")
                question = response.json()["result"][0]
            else:
                self.logger.warning("No further Node exists")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return question
    
    def navigate(self,node_name):
        result = None
        response = requests.get("{}/function/{}/navigate/{}".format(self.root_url,self.database,node_name), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                result = response.json()["result"]
            else:
                self.logger.warning("Does not exist")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return result

    def getEdgeFromTo(self,Out,In):
        result = None
        response = requests.get("{}/function/{}/getEdge/{}/{}".format(self.root_url,self.database,Out,In), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                result = response.json()["result"][0]
            else:
                self.logger.warning("Does not exist")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return result

    """
    Current decisions are : classic, qunatum. It is expected that we further expand the decision space (i.e IBM quantum hardware..etc )
    """
    def getDecisions(self):
        result = None
        response = requests.get("{}/function/{}/getDecisions".format(self.root_url,self.database), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                result = response.json()["result"]
            else:
                self.logger.warning("Does not exist")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return result

    def getVertexFromID(self,id):
        result = None
        response = requests.get("{}/function/{}/getVertexFromID/{}".format(self.root_url,self.database,id), auth = (self.username,self.password))
        if response.status_code == 200:
            if len(response.json()["result"]) > 0:
                result = response.json()["result"][0]
            else:
                self.logger.warning("Does not exist")
        else:
            self.logger.error("Error -- Status Code {}".format(response.status_code))
        return result