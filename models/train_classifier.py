# import libraries
import sys
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle

from utility.utils import tokenize


import nltk
nltk.download(['punkt', 'wordnet', 'stopwords'])


REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-zA-Z #+_]')


def load_data(database_filepath):

    """
    Load cleaned dataset from database.
    
    Input: 
        database_filepath: the name of the database to create engine and load from
    
    Output: 
        X: matrix of attributes with columes as attributes and rows as observations
        Y: target matrix, for multi-category output
        category_names: a list of all category names
    """

    # load data from database
    engine = create_engine('sqlite:///{}'.format(database_filepath))

    # run a query
    dataframe = pd.read_sql_table('DisasterResponse', engine)
    X = dataframe['message']
    Y = dataframe.drop(columns = ['message', 'genre', 'id', 'original'], axis = 1)
    
    del_cols = [i for i in Y.sum()[Y.sum().isin([0, len(Y)])].index]
    Y = Y.drop(columns = del_cols)
    category_names = Y.columns

    return X, Y, category_names


def build_model():

    """
    A machine learning pipeline contains: 
        - count vectorization 
        - tfidf transformation
        - Gradient Boosting Classification model training
        - gridsearch hyperparameters tuning
    
    Inputs: 
        None

    Output: 
        cv: pipeline represented by a GridSearchCV object
    """

    pipeline_GB = Pipeline([
            ('vect', CountVectorizer(tokenizer=tokenize)),
            ('tfidf', TfidfTransformer()),
            ('clf', MultiOutputClassifier(GradientBoostingClassifier()))
        ])
        
    
    parameters = {
        'vect__ngram_range': ((1, 1), (1, 2)),
        'clf__estimator__n_estimators': [10, 100]
    }

    cv = GridSearchCV(pipeline_GB, param_grid=parameters)
    
    return cv


def evaluate_model(model, X_test, y_test, category_names):
    '''
    Generate classification report for the model on test dataset
    
    Input: 
        model: model trained and tuned with X_train
        X_test, Y_test: test sets
        category_names: a list of all category names in Y
        
    Output: 
        - Classification report generated by sklearn.classification_report
          in each prediction category  
        - The average prediction precision, recall, and f1-score for all categories
    '''
    
    y_pred = model.predict(X_test)
    precision_list, recall_list, f1_list = [], [], []
    for i, col in enumerate(y_test.columns):
        print (i, col)
        print(classification_report(y_test[col], y_pred[:, i]))
        precision_list.append(float(classification_report(y_test[col], y_pred[:, i]).strip().split()[-4]))
        recall_list.append(float(classification_report(y_test[col], y_pred[:, i]).strip().split()[-2]))
        f1_list.append(float(classification_report(y_test[col], y_pred[:, i]).strip().split()[-3]))
        
    print ("average precision:", np.mean(precision_list))
    print ("average recall:", np.mean(recall_list))
    print ("average f1_score:", np.mean(precision_list))
  


def save_model(model, model_filepath):
    '''
    Save the trained model into a pickle file

    Input:
        model: the trained and tuned model
        model_filepath: the targeted file path for the .pkl file to be saved at
    
    Output:
        None
    '''
    
    pickle_out = open(model_filepath, 'wb')
    pickle.dump(model, pickle_out)
    pickle_out.close()


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()