"""
A module for obtaining repo readme and language data from the github API.

Before using this module, read through it, and follow the instructions marked
TODO.

After doing so, run it like this:

    python acquire.py

To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests
from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
import re

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token: https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

def get_repos():
    '''This function scrapes repository collections on github.com and returns a list 
    of url endpoints for those repositories.
    
    To use these endpoints, append each string value to 'https://github.com' to
    create a list of urls '''

    # establish a filename for the local csv
    filename = 'repos.csv'
    # check to see if a local copy already exists. 
    if os.path.exists(filename):
        print('Reading from local CSV...')
        # if so, return the local csv as a list
        repos = pd.read_csv(filename)['0']
        repos = repos.str[1:]
        return repos.to_list()
        

    #otherwise: scrape the data: 

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

REPOS = get_repos()

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        print('error from url: ', url)
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)
