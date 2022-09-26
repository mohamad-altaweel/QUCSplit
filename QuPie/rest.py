from turtle import update
import requests

class RESTacchiato():

    def __init__(self, username, password, root_url, database,logger) -> None:
        self.username = username
        self.password = password
        self.root_url = root_url
        self.database = database
        self.logger = logger

    def testConnection(self):
        response = requests.get("{}/function/{}/testConnection".format(self.root_url, self.database), auth = (self.username,self.password))
        if response.status_code == 200: 
            print("Connection success")
            return True
        else:
            print("Error -- Status code: {}".format(response.status_code))
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

    def createQuestion(self, name = "", description = "", type = ""):
        command = {"command":"INSERT INTO question(name, description, type) VALUES (:name,:description,:type)",
                   "parameters":{"name":name,"description":description,"type":type}}
        response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
        if response.status_code == 200: 
            print("Command success")
            return response
        else:
            print("Error -- Status code: {}".format(response.status_code))
            return None

    def editQuestion(self, name = "", description = "", type = ""):
        question = self.getQuestion(name)
        if question != None:
            updateCommand = "UPDATE question SET"
            whereClause = "WHERE @rid = {}".format(question["@rid"])
            parameters = {}
            if name != "":
                updateCommand =  updateCommand + "name = :name"
                parameters["name"] = name
            if description != "":
                updateCommand =  updateCommand + "description = :description"
                parameters["description"] = description
            if type != "":
                updateCommand =  updateCommand + "type = :type"
                parameters["type"] = type
            updateCommand =  updateCommand + whereClause
            command = {"command":updateCommand,"parameters":parameters}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def deleteQuestion(self, name):
        question = self.getQuestion(name)
        if question != None:
            command = "DELETE FROM question WHERE @rid = {}".format(question["@rid"])
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def createAlgorithm(self, name = "", type = ""):
        command = {"command":"INSERT INTO Algorithm(name, type) VALUES (:name,:type)",
                   "parameters":{"name":name,"type":type}}
        response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
        if response.status_code == 200: 
            print("Command success")
            return response
        else:
            print("Error -- Status code: {}".format(response.status_code))
            return None

    def editAlgorithm(self, name = "", type = ""):
        algorithm = self.getQuestion(name)
        if algorithm != None:
            updateCommand = "UPDATE Algorithm SET"
            whereClause = "WHERE @rid = {}".format(algorithm["@rid"])
            parameters = {}
            if name != "":
                updateCommand =  updateCommand + "name = :name"
                parameters["name"] = name
            if type != "":
                updateCommand =  updateCommand + "type = :type"
                parameters["type"] = type
            updateCommand =  updateCommand + whereClause
            command = {"command":updateCommand,"parameters":parameters}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return True
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return False
        else:
            return False

    def deleteAlgorithm(self, name):
        algorithm = self.getQuestion(name)
        if algorithm != None:
            command = "DELETE FROM algorithm WHERE @rid = {}".format(algorithm["@rid"])
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return True
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return False
        else:
            return False

    def createProblemClass(self, name = "", type = ""):
        command = {"command":"INSERT INTO ProblemClass(name, type) VALUES (:name,:type)",
                   "parameters":{"name":name,"type":type}}
        response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
        if response.status_code == 200: 
            print("Command success")
            return response
        else:
            print("Error -- Status code: {}".format(response.status_code))
            return None

    def editProblemClass(self, name = "", type = ""):
        problemClass = self.getQuestion(name)
        if problemClass != None:
            updateCommand = "UPDATE ProblemClass SET"
            whereClause = "WHERE @rid = {}".format(problemClass["@rid"])
            parameters = {}
            if name != "":
                updateCommand =  updateCommand + "name = :name"
                parameters["name"] = name
            if type != "":
                updateCommand =  updateCommand + "type = :type"
                parameters["type"] = type
            updateCommand =  updateCommand + whereClause
            command = {"command":updateCommand,"parameters":parameters}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def deleteProblemClass(self, name = ""):
        problemClass = self.getQuestion(name)
        if problemClass != None:
            command = "DELETE FROM ProblemClass WHERE @rid = {}".format(problemClass["@rid"])
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def createFormulation(self, name = "", type = ""):
        command = {"command":"INSERT INTO Formulation(name, type) VALUES (:name,:type)",
                   "parameters":{"name":name,"type":type}}
        response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
        if response.status_code == 200: 
            print("Command success")
            return response
        else:
            print("Error -- Status code: {}".format(response.status_code))
            return None

    def editFormulation(self, name, type):
        formulation = self.getQuestion(name)
        if formulation != None:
            updateCommand = "UPDATE Formulation SET"
            whereClause = "WHERE @rid = {}".format(formulation["@rid"])
            parameters = {}
            if name != "":
                updateCommand =  updateCommand + "name = :name"
                parameters["name"] = name
            if type != "":
                updateCommand =  updateCommand + "type = :type"
                parameters["type"] = type
            updateCommand =  updateCommand + whereClause
            command = {"command":updateCommand,"parameters":parameters}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def deleteFormulation(self, name = ""):
        formulation = self.getQuestion(name)
        if formulation != None:
            command = "DELETE FROM Formulation WHERE @rid = {}".format(formulation["@rid"])
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def createDecision(self, name = ""):
        command = {"command":"INSERT INTO decision(name) VALUES (:name)",
                   "parameters":{"name":name}}
        response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
        if response.status_code == 200: 
            print("Command success")
            return response
        else:
            print("Error -- Status code: {}".format(response.status_code))
            return None

    def editDecision(self, name):
        decision = self.getQuestion(name)
        if decision != None:
            updateCommand = "UPDATE decision SET"
            whereClause = "WHERE @rid = {}".format(decision["@rid"])
            parameters = {}
            if name != "":
                updateCommand =  updateCommand + "name = :name"
                parameters["name"] = name
            updateCommand =  updateCommand + whereClause
            command = {"command":updateCommand,"parameters":parameters}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def deleteDecision(self, name):
        decision = self.getQuestion(name)
        if decision != None:
            command = {"command":"DELETE FROM decision WHERE @rid = {}".format(decision["@rid"])}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def createAnswer(self,fromQuestion,toQuestion, name = "", description = "", hint = ""):
        fromQuestion = self.getQuestion(fromQuestion)
        toQuestion = self.getQuestion(toQuestion)
        if fromQuestion is not None and toQuestion is not None:
            command = {"command":"CREATE EDGE userAnswer FROM {} TO {} SET name =:name,description = :description,hint = :hint",
                    "parameters":{"name":name,"description":description,"hint":hint}}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def editAnswer(self, fromQuestion, toQuestion, name, description, hint):
        fromQuestion = self.getQuestion(fromQuestion)
        toQuestion = self.getQuestion(toQuestion)
        if fromQuestion != None and toQuestion != None:
            updateCommand = "UPDATE EDGE FROM {} TO {} SET ".format(fromQuestion["@rid"],toQuestion["@rid"])
            whereClause = "WHERE name = {}".format(name)
            parameters = {}
            if name != "":
                updateCommand =  updateCommand + "name = :name"
                parameters["name"] = name
            if description != "":
                updateCommand =  updateCommand + "description = :description"
                parameters["description"] = description
            if hint != "":
                updateCommand =  updateCommand + "hint = :hint"
                parameters["hint"] = hint
            updateCommand =  updateCommand + whereClause
            command = {"command":updateCommand,"parameters":parameters}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None

    def deleteAnswer(self, fromQuestion, toQuestion,  name):
        fromQuestion = self.getQuestion(fromQuestion)
        toQuestion = self.getQuestion(toQuestion)
        if fromQuestion is not None and toQuestion is not None:
            command = {"command":"DELETE EDGE FROM {} TO {} WHERE name = {}".format(fromQuestion["@rid"], toQuestion["@rid"], name)}
            response = requests.post("{}/command/{}/sql".format(self.root_url,self.database), json = command, auth = (self.username,self.password))
            if response.status_code == 200: 
                print("Command success")
                return response
            else:
                print("Error -- Status code: {}".format(response.status_code))
                return None
        else:
            return None