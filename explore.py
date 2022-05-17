import unicodedata
import re
import json
from wordcloud import WordCloud

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from prepare import *

import warnings
warnings.filterwarnings('ignore')


def words_to_counts(df):
    '''
    This function will break dataframe into words and word frequency.
    Then concate it into a DataFrame for exploration
    '''
    python_words = ' '.join(df[df.language_reduced == 'Python'].clean)
    java_words = ' '.join(df[df.language_reduced == 'JavaScript'].clean)
    html_words = ' '.join(df[df.language_reduced == 'HTML'].clean)
    other_words = ' '.join(df[df.language_reduced == 'Other'].clean)
    all_words = ' '.join(df.clean)

    py_freq = pd.Series(python_words.split()).value_counts()
    java_freq = pd.Series(java_words.split()).value_counts()
    html_freq = pd.Series(html_words.split()).value_counts()
    other_freq = pd.Series(other_words.split()).value_counts()
    all_freq = pd.Series(all_words.split()).value_counts()

    word_counts = pd.concat([py_freq, java_freq, html_freq, other_freq, all_freq], axis=1).fillna(0).astype(int)
    word_counts.columns = ['python', 'java', 'html', 'other', 'all']
    return word_counts


def longest_readme(df):
    '''
    This Function will Display the Top 20 longest readme files
    '''
    df['message_length'] = df.clean.apply(len)
    df['word_count'] = df.clean.apply(str.split).apply(len)
    print('Top 20 Longest Message')
    return df[['language_reduced', 'message_length', 'word_count']].sort_values('message_length', ascending=False).head(20)


def longest_msg_avg(df):
    '''
    This function will display all the languages and averages
    '''
    df['message_length'] = df.clean.apply(len)
    df['word_count'] = df.clean.apply(str.split).apply(len)
    print('Average Longest Message by Language')
    return round(df[['language', 'message_length', 'word_count']].groupby('language').mean().sort_values('message_length', ascending=False),2)