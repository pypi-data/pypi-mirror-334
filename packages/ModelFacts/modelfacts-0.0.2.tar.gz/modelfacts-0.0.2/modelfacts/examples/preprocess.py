# Functions for preprocessing the Titanic dataset
import re
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

def get_title(x):
    '''extract the title "Mr./Mrs." from passenger names
    Names are generally in the format "lastname, title first name
    '''
    title = x.split(r', ')[1]
    title = title.replace('the', '')
    title = title.split()[0]
    return title

def ticket_number(x):
    '''extract the ticket number'''
    try:
        num = float(x.split(" ")[-1])
    except: 
        num = np.nan
    return num
    
def ticket_item(x):
    '''extract the ticket type'''
    items = x.split(" ")
    if len(items) == 1:
        return "UNK"
    return "_".join(items[0:-1])

def cabin_letter(x):
    '''extract the cabin group
    if multiple cabins, only grabs the first'''
    if pd.isna(x):
        return 'UNK'
    else:
        items=re.split('(\d+)',x)
        return items[0]
            
def cabin_number(x):
    '''extracts the cabin number
    if multiple cabins, only grab the first'''
    if pd.isna(x):
        return np.nan
    else:
        items=re.split('(\d+)',x)
        if len(items)==1:
            return np.nan
        else:
            return float(items[1])

def preprocess_data(df):
    '''combine preprocessing functions to modify the dataframe
    returns the modified dataframe
    '''
    df['Title'] = df['Name'].apply(get_title)   
    df["Ticket_number"] = df["Ticket"].apply(ticket_number)
    df["Ticket_item"] = df["Ticket"].apply(ticket_item)     
    df['Cabin_letter'] = df['Cabin'].apply(cabin_letter)
    df['Cabin_number'] = df['Cabin'].apply(cabin_number)
    return df


def impute_data(df):
    '''fill in missing data with Unknown or median
    return modified dataframe"
    '''
    df['Embarked'] = df['Embarked'].fillna('UNK')
    df['Cabin'] = df['Cabin'].fillna('UNK')    
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    df['Cabin_number'] = df['Cabin_number'].fillna(df['Cabin_number'].median())
    df['Ticket_number'] = df['Ticket_number'].fillna(df['Ticket_number'].median())
    return df

class Columns(BaseEstimator, TransformerMixin):
    '''class to keep track of columns names after sklearn FeatureUnion'''
    def __init__(self, names=None):
        self.names = names

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X):
        return X[self.names]