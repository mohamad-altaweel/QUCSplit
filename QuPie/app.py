from flask import Flask, session, redirect, url_for, request
from logic import *
import logging
from flask import has_request_context, request
import argparse
import json
from flask_cors import CORS, cross_origin
from logic import Backbone

def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    if config is not None:
        app.config.from_file(config,load=json.load)
    else:
        raise FileNotFoundError()
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Main logger")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('info.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    backbone = Backbone(app.config["USERNAME"],app.config["PASSWORD"],app.config["ROOT_URL"],app.config["DATABASE"],logger)

    @app.route('/addQuestion' , methods = ['POST'])
    def addQuestion():
        data = request.json
        backbone.addQuestion(data["name"],data["description"],data["type"])

    @app.route('/editQuestion' , methods = ['POST'])
    def editQuestion(self):
        data = request.json
        backbone.editQuestion(data["name"],data["description"],data["type"])

    @app.route('/deleteQuestion/<name>' , methods = ['POST'])
    def deleteQuestion(self, name = ""):
        backbone.deleteQuestion(name)

    @app.route('/addProblemClass' , methods = ['POST'])
    def addProblemClass(self):
        data = request.json
        backbone.addProblemClass(data["name"], data["type"])

    @app.route('/editProblemClass' , methods = ['POST'])
    def editProblemClass(self):
        data = request.json
        backbone.editProblemClass(data["name"], data["type"])

    @app.route('/deleteProblemClass/<name>' , methods = ['POST'])
    def deleteProblemClass(self , name = ""):
        backbone.deleteProblemClass(name)

    @app.route('/addFormulation' , methods = ['POST'])
    def addFormulation(self):
        data = request.json
        backbone.addFormulation(data["name"], data["type"])

    @app.route('/editFormulation' , methods = ['POST'])
    def editFormulation(self, name, type):
        data = request.json
        backbone.editFormulation(data["name"], data["type"])

    @app.route('/deleteFormulation/<name>' , methods = ['POST'])
    def deleteFormulation(self, name = ""):
        backbone.deleteFormulation(name)

    @app.route('/addAlgorithm' , methods = ['POST'])
    def addAlgorithm(self):
        data = request.json
        backbone.addAlgorithm(data["name"], data["type"])

    @app.route('/editAlgorithm' , methods = ['POST'])
    def editAlgorithm(self, name = "", type = ""):
        data = request.json
        backbone.editAlgorithm(data["name"], data["type"])

    @app.route('/deleteAlgorithm/<name>' , methods = ['POST'])
    def deleteAlgorithm(self, name = ""):
        backbone.deleteAlgorithm(name)

    @app.route('/addDecision' , methods = ['POST'])    
    def addDecision(self):
        data = request.json
        backbone.addDecision(data["name"])

    @app.route('/editDecision' , methods = ['POST'])  
    def editDecision(self, name  = ""):
        data = request.json
        backbone.editDecision(data["name"])

    @app.route('/deleteDecision/<name>' , methods = ['POST'])
    def deleteDecision(self , name = ""):
        backbone.deleteDecision(name)

    @app.route('/addAnswer' , methods = ['POST'])    
    def addAnswer(self):
        data = request.json
        backbone.addAnswer(data["fromQuestion"], data["toQuestion"], data["name"], data["description"], data["hint"])

    @app.route('/editAnswer' , methods = ['POST'])  
    def editAnswer(self, name  = ""):
        data = request.json
        backbone.editAnswer(data["fromQuestion"], data["toQuestion"], data["name"], data["description"], data["hint"])

    @app.route('/deleteAnswer' , methods = ['POST'])
    def deleteAnswer(self):
        data = request.json
        backbone.deleteAnswer(data["fromQuestion"], data["toQuestion"], data["name"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcoem to QuPie app')
    parser.add_argument('config', type=str,help='A required path for config.json file')
    args = parser.parse_args()
    app = create_app(args.config)
    app.run(host="0.0.0.0")