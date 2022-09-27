# QuCSplit
QuCSplit is a decision support framework to aid stakeholders from different industrial as well research fields by providing the recommendation to use quantum or classical computing for a given use case based on set of interactive questionnaire or similar entries in the knowledge base. This project is part of Master thesis at the Institute of architecutre of application system in the University of Stuttgart

## System Architecture
The framework consists of four main components as shown in the diagram 
- orientDb : An open-source DBMS for graph databases, in which we save the facts in form of connected verticies. The database can be accessed through an interactive studio, which we can visualize the graph database.
- QuCMixx : Backend service which retrives information and decision from the knowledge base depending on user inputs.
User can provide the requirements as answers to an interactive questionaire or full description submission.
- QuPie : Backend service to add, edit, delete facts and handle information in the knowledge base.
- QuCface : Frontend sites to communicate with QuCMixx

![QuCSplit framework Architecture](/docs/img/QUCarch.png "System Architecture")

You can refer to each service document for a full details

## How to run

for an easy installation and deployment, we dockerized each service in seperated containers. Refer [How-to](/docs/how-to.md) to run the framework.

## Contribution

We welcome every contribution to our system. Aim of QuCSplit is to be a reference for users to help them in the decision process of selection of classical or quantum computing for their use case. Hence, we consider two types of contribution.

- Technical contribution: The system implements a microservice based Architecutre. Each component is implemented as micorservice where they communicate through REST API. Hence, we focus on the extendiblity whether by adding new components or maintaining the current one. Please refer to each service document where its structured and defined endpoints are defined
- Knowledge contribution: Information are retrieved from expirmentes done comparing between classical and quantum methods to solve a specifc use case. Please refer to the [Database](/docs/database.md) to know more about the database structure and how to model the knowledge in form of question & answers to add in the knowledge base

## Thesis Link
QuCSplit: A Decision Support System for Quantum-Classical Splitting, Mohamad Altaweel [Link](#)

