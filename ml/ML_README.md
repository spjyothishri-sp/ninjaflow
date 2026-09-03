\# NinjaFlow ML Module



\## Overview



The NinjaFlow ML module predicts payment delays and calculates liquidity risk for supply-chain entities.



All data used in this prototype is 100% synthetic and does not contain real customer or company data.



\## Files



\- generate\_dataset.py - Generates synthetic transaction data

\- features.py - Performs feature engineering

\- train\_model.py - Trains the Random Forest model

\- predict.py - Loads the trained model and performs predictions

\- model.pkl - Trained Random Forest model



\## Model



Model: Random Forest Regressor



Target:

label\_delay\_days



The model predicts the expected number of payment delay days.



\## Features



The model uses 10 features:



1\. historical\_average\_delay

2\. current\_cash

3\. outstanding\_receivables

4\. upcoming\_payables

5\. order\_frequency\_per\_month

6\. season\_index

7\. order\_amount

8\. invoice\_amount

9\. days\_since\_transaction

10\. credit\_term\_days



\## Prediction Function



The backend can import the prediction function from `predict.py`.



Example:



from predict import predict\_delay



features = {

&#x20;   "historical\_average\_delay": 5.0,

&#x20;   "current\_cash": 150000,

&#x20;   "outstanding\_receivables": 250000,

&#x20;   "upcoming\_payables": 180000,

&#x20;   "order\_frequency\_per\_month": 12,

&#x20;   "season\_index": 0.6,

&#x20;   "order\_amount": 50000,

&#x20;   "invoice\_amount": 50000,

&#x20;   "days\_since\_transaction": 30,

&#x20;   "credit\_term\_days": 15

}



result = predict\_delay(features)



The result contains:



\- predicted\_delay\_days

\- delay\_probability

\- risk\_score

\- risk\_level



\## Current Model Evaluation



Training rows: 2400



Testing rows: 600



Mean Absolute Error: approximately 5.05 days



The model is intended as a hackathon prototype using synthetic data.



\## Important



NinjaFlow is a prototype.



All financial figures and predictions shown in the application are simulated demo data.



Ninjacart is used only as an unaffiliated case-study reference and is not connected to this prototype.

