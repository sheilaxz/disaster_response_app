import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):

    """
    Load raw datasets and merge them together by column "id".
    
    Input: 
        None

    Output: 
        merged dataset
    """

    # load messages dataset
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    # merge datasets
    df = messages.merge(categories, left_on = 'id', right_on = 'id')
    return df


def clean_data(df):

    """
    Generate a cleaned dataset
    
    Input: 
        Merged dataset generated from raw datasets using function load_data()

    Output: 
        Cleaned dataset 
            - Original Y (category column) is converted to 36 binary columns
    """


    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(';', expand = True)

    # select the first row of the categories dataframe
    row = categories.iloc[0, :]

    # use this row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything 
    # up to the second to last character of each string with slicing
    category_colnames = list(map(lambda x: x[:-2], row))

    # rename the columns of `categories`
    categories.columns = category_colnames

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = list(map(lambda x: x[-1], categories[column]))
    
        # convert column from string to numeric
        categories[column] = list(map(int, categories[column]))

    # drop the original categories column from `df`
    df = df.drop(columns = ['categories'])

    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis = 1)

    # drop duplicates
    filt = df.duplicated()
    df = df[~filt]
    return df


def save_data(df, database_filename):

    ### load to database

    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('DisasterResponse', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
