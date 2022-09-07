import yake
from nltk.tokenize import word_tokenize
import math
from ordered_set import OrderedSet
import json 
import os
import logging


"""
Compare Between a set of documents of reference use cases and a new use case through Cosine Similarity measure
Class include methods from reading the file, construction of document vector, and computing the cosine similarity 
@required_libaray: YAKE, NLTK, OrderedSet
"""
class RefCaseComparator():

    def __init__(self) -> None:
        self.custom_kw_extractor = yake.KeywordExtractor(n = 2 ,top=20)
        self.all_words = None
        self.encoded_vectors = []
        self.vectors = []
        self.documents = []

    """
    Yake returns the keywords in form of list of tuples where each tuple is the keyword with its impact measure
    returns all the keywords as a list.
    """
    def getKeywordsVector(self,yakeOutput):
        results = []
        for k in yakeOutput:
            results.append(k[0])
        return results

    def detectProblemclass(self,text,vector):
        problemsclasses = ["SAT", "TSP", "Max-Cut","MIS","partioning"]
        tokenizedText = word_tokenize(text)
        for problem in problemsclasses:
            if problem in tokenizedText:
                vector.append(problem)

    def detectFormulation(self,text,vector):
        formulations = ["QUBO", "PUBO", "Graph"]
        tokenizedText = word_tokenize(text)
        for problem in formulations:
            if problem in tokenizedText:
                vector.append(problem)

    def detectAlgorithm(self,text,vector):
        algorithms = ["QA", "QAOA", "VQE","GAS","HHL","DQC","QNN","QPE"]
        tokenizedText = word_tokenize(text)
        for problem in algorithms:
            if problem in tokenizedText:
                vector.append(problem)

    """
    build the glossary index of all found keywords from all reference use cases
    """
    def getWordsGloassary(self,listOfKeywords):
        keywords = OrderedSet()
        for keyword_vector in listOfKeywords:
            for keyword in keyword_vector:
                keywords.add(keyword)
        return keywords

    """
    encode each document to a one-hot-encoding vector where each component includes where keyword in document (1) or not (0)
    Problem class, formulation, and algorithm keywords have stronger impact on simialrity when mentioned in text
    We define Weights for them 
    Problem class : 2, Formulation : 3, Algorithm : 4
    the encoded vector is normalized
    """
    def encodeVectorAsOnehot(self,keyword_vector, words):
        encoded_vector = [0] * len(words)
        problemsclasses = ["SAT", "TSP", "Max-Cut","MIS","partioning"]
        formulations = ["QUBO", "PUBO", "Graph"]
        algorithms = ["QA", "QAOA", "VQE","GAS","HHL","DQC","QNN","QPE"]
        for keyword in keyword_vector:
            if keyword in words:
                index = words.index(keyword)
                weight = 1 / 4
                if keyword in problemsclasses:
                    weight = 2 / 4
                elif keyword in formulations:
                    weight = 3 / 4
                elif keyword in algorithms:
                    weight = 4 / 4
                encoded_vector[index] = weight
        return encoded_vector

    def compute_cosine_similarity(self, firstVector, secondVector):
        sum = 0
        for i in range(len(firstVector)):
            sum = sum + (firstVector[i] * secondVector[i])
        magnitudeOne = 0
        magnitudeTwo = 0
        for i in range(len(firstVector)):
            magnitudeOne = magnitudeOne + (firstVector[i] * firstVector[i])
        for i in range(len(secondVector)):
            magnitudeTwo = magnitudeTwo + (secondVector[i] * secondVector[i])
        return sum / (math.sqrt(magnitudeOne) * math.sqrt(magnitudeTwo))

    def read_usecase(self,filepath):
        with open(filepath) as f:
            data = json.load(f,strict=False)
            return data

    """
    read all use cases in the given folder
    build glossary index
    encode each use case
    """
    def BuildKeywordsVectorsForEachDocument(self,folderpath):
        listOfFiles = os.listdir(folderpath)
        for file in listOfFiles:
            data = self.read_usecase(folderpath + "/" + file)
            self.documents.append(data)
        for document in self.documents:
            keywords = self.custom_kw_extractor.extract_keywords(document["description"])
            keywords_vector = self.getKeywordsVector(keywords)
            del keywords
            self.detectProblemclass(document["description"],keywords_vector)
            self.detectFormulation(document["description"],keywords_vector)
            self.detectAlgorithm(document["description"],keywords_vector)
            self.vectors.append(keywords_vector)
        self.all_words = self.getWordsGloassary(self.vectors)
        for vector in self.vectors:
            encodedVector = self.encodeVectorAsOnehot(vector,self.all_words)
            self.encoded_vectors.append(encodedVector)

    """
    compute for a given new document the cosine simialrity with all other use cases
    @return: list of cosine simialirty for each docment with the new use case
    """    
    def getCosSimilarityRanking(self,toCompare):
        ranking = []
        keywords = self.custom_kw_extractor.extract_keywords(toCompare)
        keywords_vector = self.getKeywordsVector(keywords)
        self.detectProblemclass(toCompare,keywords_vector)
        self.detectFormulation(toCompare,keywords_vector)
        self.detectAlgorithm(toCompare,keywords_vector)
        encoded_vector = self.encodeVectorAsOnehot(keywords_vector,self.all_words)
        for vector in self.encoded_vectors:
            cosSim = self.compute_cosine_similarity(encoded_vector,vector)
            ranking.append(cosSim)
        return ranking
    
    """
    get the biggest cosine measure, index of its use case, and get the cosine simialrity of context between both cases for more extracted keyword
    """
    def getSimilarCase(self,text):
        ranking = self.getCosSimilarityRanking(text)
        maxCosSimialrity = max(ranking)
        indexSimilarDocument = ranking.index(maxCosSimialrity)
        similarDocument = self.documents[indexSimilarDocument]
        exactness = self.getPercentageOfCommonWords(text,similarDocument["description"])
        return maxCosSimialrity,similarDocument,exactness
    
    def getPercentageOfCommonWords(self,firstText,secondText):
        count = 0
        kw_extractor = yake.KeywordExtractor(n = 2 ,top=30)
        yakeOutputFirst = kw_extractor.extract_keywords(firstText)
        keywordsFirstVector = self.getKeywordsVector(yakeOutputFirst)
        yakeOutputSecond = kw_extractor.extract_keywords(secondText)
        keywordsSecondVector = self.getKeywordsVector(yakeOutputSecond)
        for i in range(len(keywordsFirstVector)):
            if keywordsFirstVector[i] in keywordsSecondVector:
                count = count + 1
        return (count / 30) * 100

    