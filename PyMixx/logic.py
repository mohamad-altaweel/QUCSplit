from rest import RESTpresso
from flask import has_request_context, request

"""
Backbone interacts with rest passing the right answer depending on the type of question/answer it retrieves
"""
class Backbone:

    def __init__(self,username,password,url,database,logger) -> None:
        self.logger = logger
        self.rest = RESTpresso(username,password,url,database,self.logger)
        self.rest.testConnection()

    """Answer a question with a single choice"""
    def answerSingleChoiceQuestion(self,question,answer):
        remoteAddress = request.remote_addr if has_request_context() else "Unknown"
        answers = self.rest.GetPossibleAnswers(question["name"])
        possible = self.getAnswerFromName(answers,answer)
        node = self.rest.getNextNode(possible["@rid"][1:])
        Nextanswers = self.rest.GetPossibleAnswers(node["name"])
        if node["@class"] == "decision":
            # here we reach a final decision
            self.logger.info("User: {} has reached a final decision".format(remoteAddress))
            return {"question":"Off","answers": node["name"]}
        elif len(Nextanswers) == 0 and node["@class"] is not "decision" :
            # we reached a Vertex where no information can be given further and it isnot a final decision (dead end)
            self.logger.info("User: {} has reached a dead end".format(remoteAddress))
            return {"question":"Dead","answers": []}
        else:
            # get the next question and its possible answers
            return {"question":node,"answers":Nextanswers}

    """Answer a question with a given integer value"""
    def answerNumberGivenQuestion(self,question,answer):
        answers = self.rest.GetPossibleAnswers(question["name"])
        remoteAddress = request.remote_addr if has_request_context() else "Unknown"
        Node = None
        if int(answer) > int(question["decision"]):
            Node = self.getAnswerFromName(answers, "MoreThan{}".format(int(question["decision"])))
        else:
            Node = self.getAnswerFromName(answers, "LessThan{}".format(int(question["decision"])))
        nextNode = self.rest.getNextNode(Node["@rid"][1:])
        Nextanswers = self.rest.GetPossibleAnswers(Node["name"])
        if nextNode["@class"] == "decision":
            # here we reach a final decision
            self.logger.info("User: {} has reached a final decision".format(remoteAddress))
            return { "question":"Off", "answers": nextNode["name"] }
        elif len(Nextanswers) == 0 and nextNode["@class"] is not "decision" :
            # we reached a Vertex where no information can be given further and it isnot a final decision (dead end)
            self.logger.info("User: {} has reached a dead end".format(remoteAddress))
            return { "question":"Dead","answers": []}
        else:
            return {"question":nextNode,"answers":Nextanswers}

    def getFirstQuestion(self):
        firstQuestion = self.rest.getQuestion("YourProblemDomain")
        answers = self.rest.GetPossibleAnswers("YourProblemDomain")
        return {"question":firstQuestion,"answers":answers}
        
    def getAnswerFromName(self,answers,name):
        for possible in answers:
            if possible["name"] == name:
                return possible
            else:
                pass

    """Add a answer only if it is new to the list"""
    def AddNewAnswerToList(self,list,newAnswer):
        isNew = True
        for i in range(len(list)):
            if newAnswer[0] == list[i][0]:
                list[i] = newAnswer
                isNew = False
        if isNew:
            list.append(newAnswer)
        
    """
    Get all possible cases from a given point to reach a decision
    """
    def getAllpossible(self,currentnode):
        all_decisions = self.rest.getDecisions()
        all_paths = self.rest.navigate(currentnode)
        final_paths = []
        output = []
        for path in all_paths:
            p = path["$path"]
            for d in all_decisions:
                if d["@rid"] in p:
                    final_paths.append(p)
                    break
        for path in final_paths:
            for i in range(len(path) - 1):
                v = self.rest.getVertexFromID(path[i][1:])
                e = self.rest.getEdgeFromTo(path[i][1:],path[i+1][1:])
                if "description" in v:
                    output.append((v["description"],e["name"],v["name"]))
                else:
                    output.append((v["name"],e["name"],v["name"]))
            v = self.rest.getVertexFromID(path[-1][1:])
            output.append(("decision",e["name"],v["name"]))
        return output

    def getQuestion(self,question):
        return self.rest.getQuestion(question)

    def quesionExists(self,question):
        return self.rest.QuestionExists(question)

    def getAllpossibleAnswers(self,question):
        return self.rest.GetPossibleAnswers(question)
    
    def getNextNode(self,edgeId):
        return self.rest.getNextNode(edgeId)