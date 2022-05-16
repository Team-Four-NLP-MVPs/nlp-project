# unicode, regex, json for text digestion
import unicodedata
import re
import json
from wordcloud import WordCloud

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# nltk: natural language toolkit -> tokenization, stopwords (more on this soon)
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

from prepare import *


# pandas dataframe manipulation, acquire script, time formatting
import pandas as pd
from time import strftime

# shh, down in front
import warnings
warnings.filterwarnings('ignore')


def words_to_counts(df):
    
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