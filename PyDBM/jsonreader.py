import json

class JSONboost():

    def readJSON(fileName):
        with open(fileName) as f:
            data = json.load(f)
            return data

    def turnToJSON(dict):
        return json.dumps(dict)    