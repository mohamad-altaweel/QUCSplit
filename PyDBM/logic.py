from os import name
from rest import RESTpresso
from jsonreader import JSONboost
from rest import RESTacchiato

"""
Backbone interacts with rest passing the right answer depending on the type of question/answer it retrieves
"""
class Backbone:

    def __init__(self,username,password,url,database,logger) -> None:
        self.logger = logger
        self.rest = RESTacchiato(username,password,url,database,self.logger)
        self.rest.testConnection()

    def addQuestion(self, name = "", description  = "", type  = ""):
        self.rest.createQuestion(name,description,type)

    def editQuestion(self, name = "" ,description = "", type = ""):
        self.rest.editQuestion(name, description, type)

    def deleteQuestion(self, name = ""):
        self.rest.deleteQuestion(name)

    def addProblemClass(self, name = "", type = ""):
        self.rest.createProblemClass(name, type)

    def editProblemClass(self, name = "", type  = ""):
        self.rest.editProblemClass(name, type)

    def deleteProblemClass(self , name = ""):
        self.rest.deleteProblemClass(name)

    def addFormulation(self, name = "", type = ""):
        self.rest.createFormulation(name, type)

    def editFormulation(self, name, type):
        self.rest.editFormulation(name, type)

    def deleteFormulation(self, name = ""):
        self.rest.deleteFormulation(name)

    def addAlgorithm(self, name = "", type = ""):
        self.rest.createAlgorithm(name, type)

    def editAlgorithm(self, name = "", type = ""):
        self.rest.editAlgorithm(name, type)

    def deleteAlgorithm(self, name = ""):
        self.rest.deleteAlgorithm(name)
    
    def addDecision(self, name = ""):
        self.rest.createDecision(name)

    def editDecision(self, name  = ""):
        self.rest.editDecision(name)

    def deleteDecision(self , name = ""):
        self.rest.deleteDecision(name)



