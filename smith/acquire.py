from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
import re

def get_endpoints():
    '''This function scrapes repository collections on github.com and returns a list 
    of url endpoints for those repositories.
    
    To use these endpoints, append each string value to 'https://github.com' to
    create a list of urls '''
    # create an empty list to store endpoints
    endpoints = []
    # go to each url - trending repos daily, weekly, and monthly
    for url in ['https://github.com/trending?since=daily&spoken_language_code=en',
                'https://github.com/trending?since=weekly&spoken_language_code=en',
                'https://github.com/trending?since=monthly&spoken_language_code=en']:
        # get the response
        response = get(url)
        # create the beautiful soup object
        soup = BeautifulSoup(response.text, 'html.parser')
        # identify html objects containing each repository
        for repo in soup.select('.Box-row'):
            # pull out the url endpoint for that repo and append to the list
            endpoints.append(repo
                             .select_one('h1')
                             .select_one('a')
                             .attrs['href'])
    # head to a new set of repo collections and repeat the process
    for url in ['https://github.com/collections/learn-to-code',
                'https://github.com/collections/open-source-organizations']:
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for repo in soup.select('article'):
            endpoints.append(repo
                                .select_one('h1')
                                .select_one('a')
                                .attrs['href'])
    # return the list of endpoints
    return endpoints