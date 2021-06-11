### Table of Contents

1. [Introduction](#intro)
2. [File Description](#files)
3. [Heroku Web App](#webapp)
4. [Licensing, Authors, and Acknowledgements](#licensing)
5. [Other resources](#others)

## 1. Introduction <a name="intro"></a>

This project is an analysis of disaster data from Figure Eight to build a model for an API that classifies disaster messages.  

The data set contains real messages that were sent during disaster events. A machine learning pipeline is created to categorize these events into 36 categories, so that the messages can be sent to an appropriate disaster relief agency.  

The machine learning pipeliine includes natural language processing (text processing), feature extraction, modeling, and Flask web app development. In the [web app](https://disaster-response-ml-project.herokuapp.com/), one can input a new message and get classification results. The web app also displays visualizations of the training dataset.  

## 2. File Description <a name="files"></a>

### Raw datasets and data processing

There are two raw datasets used for model training and testing: "./data/disaster_messages.csv" contains raw text messages, and "./data/disaster_categories.csv" contains response categories for each piece of text message in the previous .csv file. 

"./data/process_data.py" is the text data processing pipeline used in this step. The pipeline includes:  

- Loading and merging the original two .cvs datasets  
- Cleaning the merged dataset  
- Saving the processed dataset into a database named "DisasterResponse.db" for later use in Machine Learning pipeline  

"./data/DisasterResponse.db" is the processed database saved after the data processing ETL pipeline.  


### Machine learning pipeline

With the cleaned dataset, a machine learning pipeline is created to train a classification model, such that future text input could be processed and classified.  

"./models/train_classifier.py" is the machine learning pipeline used in this step. The pipeline includes:

- Loading data from the database generated in the previous data processing step, and spliting the data into training and testing sets  
- Building a Gradient Boosting Classification model with sklearn package, and tuning the model with GridSearchCV package  
- Evaluating the model based on prediction precision, recall, and f1-score  
- Saving the trained and tuned model into a pickle file named "classfier.pkl"

A separate file named "utils.py" can be found in folder "utility," where the tokenize function is saved and imported from in the pipeline.


### Deployment

To install the flask app locally on your computer, you need:  

- python3  
- python packages in the [requirements.txt](https://github.com/sheilaxz/disaster_response_app/blob/main/requirements.txt) file  

Install the packages with
```
pip install -r requirements.txt
```

Run the following command in the app's directory "./application" to run the web app.
```
python run.py
```


## 3. Heroku Web App <a name="webapp"></a>

One may access the web app [here](https://disaster-response-ml-project.herokuapp.com/). It might take a while to load the page.  

To use the app, enter a piece of message (in English) in the text box, and click the "Classify Message" button. The app will automatically process text data and return relevant categories.


## 4. Licensing, Authors, and Acknowledgements <a name="licensing"></a>

Must give credits to: 
- Figure Eight, who kindly provides the raw datasets, and 
- Udacity, who guides through this natural language processing project

Also give credits to Rajat S., a mentor of the Udacity Data Science Nanodegree program, helped solve issues in the deployment process.


## 5. Other resources <a name="others"></a>

More details of the process of creating the two pipelines (data processing and machine learning) can be found [here](https://github.com/sheilaxz/disaster_response) in two Jupyter notebooks "ETL Pipeline Preparation.ipynb" and "ML Pipeline Preparation.ipynb." This github repository includes files to generate the same disaster response app locally.