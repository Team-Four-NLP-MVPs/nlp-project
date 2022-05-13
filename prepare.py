import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd
from sklearn.model_selection import train_test_split
random_state = 42

def basic_clean(text):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    text = re.sub(r"[^a-z0-9'\s]", '', text)
    return text

def tokenize(text):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(text, return_str=True)

def stem(text):
    ps = nltk.porter.PorterStemmer()
    words = text.split()
    stems = [ps.stem(word) for word in words]
    return ' '.join(stems)

def lemmatize(text):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    return ' '.join(lemmas)

def remove_stopwords(text, stopword_list=stopwords.words('english')):
    words = text.split()
    filtered_words = [word for word in words if word not in stopword_list]
    return ' '.join(filtered_words)

def nlp_prep(df):
    df = df.rename(columns={'content':'original'})
    df['clean'] = (df.original.apply(basic_clean)
                     .apply(tokenize)
                     .apply(remove_stopwords)
                  )
    df['stemmed'] = df.clean.apply(stem)
    df['lemmatized'] = df.clean.apply(lemmatize)
    return df

def prep_repos(df):
    '''takes in df created from data.json and performs nlp
    preparation steps'''
    df = df.rename(columns={'readme_contents':'original'})
    df = nlp_prep(df)
    return df

def train_validate_test_split(x, y, test_size=.2, validate_size=.3, random_state=random_state):
    '''
    This function takes in x and y, then splits each of them into three separate samples: 
    train, test, and validate, for use in machine learning modeling.

    The samples are returned in the following order: 
         x_train, y_train, x_validate, y_validate, x_test, y_test
    
    The function also prints the size of each sample.
    '''
    # split x into train and test
    x_train, x_test = train_test_split(x, test_size=test_size, random_state=random_state)
    # further split the x_train into train and validate
    x_train, x_validate = train_test_split(x_train, test_size=validate_size, random_state=random_state)

    # split y into train and test
    y_train, y_test = train_test_split(y, test_size=test_size, random_state=random_state)
    # further split the y_train into train and validate
    y_train, y_validate = train_test_split(y_train, test_size=validate_size, random_state=random_state)


    # print the size of each resulting sample
    print(f'train\t n = {x_train.shape[0]}')
    print(f'train\t n = {y_train.shape[0]}')
    print(f'validate n = {x_validate.shape[0]}')
    print(f'train\t n = {y_validate.shape[0]}')
    print(f'test\t n = {x_test.shape[0]}')
    print(f'train\t n = {y_test.shape[0]}')
    

    return x_train, y_train, x_validate, y_validate, x_test, y_test