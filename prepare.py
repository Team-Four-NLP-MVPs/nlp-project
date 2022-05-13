#|---------------------------------------------------------------------------------------------|#
#   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄   #
#  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  #
#  ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀   #
#  ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌            #
#  ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄   #
#  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  #
#  ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀   #
#  ▐░▌          ▐░▌     ▐░▌  ▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌            #
#  ▐░▌          ▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌          ▐░▌       ▐░▌▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄   #
#  ▐░▌          ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌  #
#   ▀            ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀            ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀   #
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
# A module for preparing READMEs from repositories as well as language data from the github API.#
#                  Before using this module, please do the following:                           #
# *Ensure all pre-requisite steps for token credentials(see acquire.py) are fulfilled.          #
#                    User-Defined Functions present in this script:                             #
# * basic_clean, tokenize, stem, lemmatize, remove_stopwords,                                   #
#   nlp_prep, prep_repos, train_validate_test_split                                             #
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
#                                           IMPORTS                                             #
import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd
from sklearn.model_selection import train_test_split
random_state = 42
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
#                                    USER-DEFINED FUNCTIONS                                     #
def basic_clean(text):
    """
    Receives a string of text, processes it & then returns its normalized version.
    Normalization via standard NKFD unicode, fed into an asii encoder & decoded back into UTF-8.
    """
    # .lower converts all alphabetic characters to lower-case
    text = text.lower()
    # Returns: normal form for the Unicode string; UTF-8 encoded version of the string in ASCII.
    # In the event of an error, ignores the unencodable unicode from the result.
    # decodes the string using the codec registered for encoding: UTF-8.
    text = unicodedata.normalize('NFKD', text)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    # Return: string obtained by replacing leftmost non-overlapping patterns by the replacement.
    text = re.sub(r"[^a-z0-9\s]", '', text)
    return text
#|---------------------------------------------------------------------------------------------|#
def tokenize(text):
    """This function takes in a string and returns it in its tokenized form."""
    # Create the tokenizer. The tok-tok tokenizer is a simple, general tokenizer...
    # where the input has one sentence per line; thus only the final period is tokenized.
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # Use the tokenizer's tokenization to the inputted string, ensure it returns as a string.
    return tokenizer.tokenize(text, return_str=True)
#|---------------------------------------------------------------------------------------------|#
def stem(text):
    """
    Stemmers remove morphological affixes from words, leaving only the word stem.
    As such, this UDF is applied on a word-by-word basis, deciding what the conjugation
    is doing which aspect should be cut off. Looping or list-comprehension is 
    needed to handle multiple texts in a single executable line, and is included here.
    """
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    # split by the default, which is a single space. 
    words = text.split()
    # use list-comprehension +> stem each word for the words inside the entire document
    stems = [ps.stem(word) for word in words]
     # Join our lists of words into a string again and return the outcome.
    return ' '.join(stems)
#|---------------------------------------------------------------------------------------------|#
def lemmatize(text):
    """
    Lemmatization in linguistics is the process of grouping together the inflected forms
    of a word so they can be analysed as a single item, identified by the word's lemma,
    or dictionary form. This UDF algorithmically processes string and determine the lemma
    of a word based on its intended meaning. It then returns the lemmas.
    """
    # Create the Lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    # use list-comprehension to lemmatize every word.
    # text.split() => output a list of every token in the document
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    # Join our lists of words into a string again and return the outcome
    return ' '.join(lemmas)
#|---------------------------------------------------------------------------------------------|#
def remove_stopwords(text, stopword_list=stopwords.words('english')):
    '''
    This function takes in some text, optional extra_words and exclude_words parameters
    with default empty lists and returns the text after removing all stop words.
    An alternate version of this can be created/used without the inclusion of casting to set-type.  
    '''
    # split words provided in argument
    words = text.split()
    # filter these words according to whether or not stopwords appear
    filtered_words = [word for word in words if word not in stopword_list]
    # return the results
    return ' '.join(filtered_words)
#|---------------------------------------------------------------------------------------------|#
def nlp_prep(df):
    """
    This UDF processes a DataFrame. Returns a DataFrame with the following aspects:
    original content & text stemmed, lemmatized, cleaned, tokenized, & w/ stopwords removed.
    """
    # renames content to indicate it is the original variant
    df = df.rename(columns={'content':'original'})
    # create a column called 'clean' with the previously established UDFs.
    df['clean'] = (df.original.apply(basic_clean)
                     .apply(tokenize)
                     .apply(remove_stopwords)
                  )
     # create a column called 'stemmed' with the previously established UDFs.
    df['stemmed'] = df.clean.apply(stem)
     # create a column called 'lemmatized' with the previously established UDFs.
    df['lemmatized'] = df.clean.apply(lemmatize)
    return df
#|---------------------------------------------------------------------------------------------|#
def prep_repos(df):
    '''Processes DataFrame created from 'data.json' and performs NLP preparation steps'''
    # renames content to indicate it is the original variant
    df = df.rename(columns={'readme_contents':'original'})
    # performs stemming, lemmatization, and cleaning from previous UDF.
    df = nlp_prep(df)
    return df
#|---------------------------------------------------------------------------------------------|#
def split_data(df, target):
    '''
    This function takes in a dataframe and splits it into train, test, and 
    validate dataframes for while stratifying along the target.
    '''

    train_validate, test = train_test_split(df, test_size=.2, random_state=random_state, 
                                            stratify=df[target])
    train, validate = train_test_split(train_validate, test_size=.3, 
                                       random_state=random_state, stratify=df[target])

    # print the size of each resulting sample
    print(f'train\t n = {train.shape[0]}')
    print(f'validate n = {validate.shape[0]}')
    print(f'test\t n = {test.shape[0]}')
    
    return train, validate, test
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#