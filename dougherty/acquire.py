#|---------------------------------------------------------------------------------------------|#
#   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄   #
#  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  #
#  ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀   #
#  ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░▌       ▐░▌▐░▌            #
#  ▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄   #
#  ▐░░░░░░░░░░░▌▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  #
#  ▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌     ▐░▌     ▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀   #
#  ▐░▌       ▐░▌▐░▌          ▐░░░░░░░░░░░▌▐░▌       ▐░▌     ▐░▌     ▐░▌     ▐░▌  ▐░▌            #
#  ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄  ▀▀▀▀▀▀█░█▀▀ ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄█░█▄▄▄▄ ▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄   #
#  ▐░▌       ▐░▌▐░░░░░░░░░░░▌        ▐░▌  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌  #
#   ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀          ▀    ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀   #
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
# A module for obtaining READMEs from repositories as well as language data from the github API.#
# Before using this module, please do the following:                                            #
# FIRST, make a GitHub personal access token here - https://github.com/settings/tokens          #
#       Do not select any scopes in this process; leave all boxes unticked.                     #
#       Save the token credentials in your env.py file under the variable `github_token`        #
# SECOND, add your github username to your env.py file under the variable `github_username`     #
# THIRD, Add more repositories to the `REPOS` list below.                                       #
#                                                                                               #
# AFTER THESE THREE STEPS ARE COMPLETE --> Use the terminal to run: python acquire.py           #
# This will result in the creation of a 'data.json' file containing the results of the scrape.  #
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
#                                           IMPORTS                                             #
# User-dependent imports                                                                        #
from env import github_token, github_username                                                   #
import os                                                                                       #
# Standard-fare                                                                                 #
import pandas as pd                                                                             #
import numpy as np                                                                              #
# NLP Necessities                                                                               #
from typing import Dict, List, Optional, Union, cast                                            #
import requests                                                                                 #
from requests import get                                                                        #
from bs4 import BeautifulSoup                                                                   #
# Others                                                                                        #
import json                                                                                     # 
import re                                                                                       #
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
#                                    USER-DEFINED FUNCTIONS                                     #
def get_repos():
    '''
    This function scrapes repository collections on github.com and returns a list 
    of url endpoints for those repositories.
    
    To use these endpoints, append each string value to 'https://github.com' to
    create a list of urls.
    '''
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
        # create the beautiful soup object; It creates a parse tree from page source code
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
REPOS.append(['liu513632815/WebCustomerService',
              'awslabs/aws-customer-churn-pipeline',
              'chawucirencc/Predicting-whether-a-telecommunications-company-is-losing-customers',
              'ameerbadri/amazon-alexa-twilio-customer-service',
              'bplank/ijcnlp2017-customer-feedback',
              'likeastore/ngCustomerVoice',
              'KolatimiDave/Expresso-Customer-Churn-Prediction',
              'codingmonk21/CustomerSupportDesk',
              'sol-eng/customer-tracker',
              'mageplaza/magento-2-customer-approval',
              'iris9112/Customer-Segmentation',
              'quafzi/magento-CustomerGridOrderCount',
              'AatiqUrRehman/customer-support-flutter-ui',
              'vercel/customer-support-examples',
              'customerio/go-customerio',
              'nexmo-community/nexmo-customer-service-chat-demo'])
# Headers which grant authorization for scraping the APIs
headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}
# Failsafe indicating the necessary pre-requisities have not been performed
if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )
#|---------------------------------------------------------------------------------------------|#

def github_api_request(url: str) -> Union[List, Dict]:
    """
    Using the requests library, this UDF pings the provided URL
    obtains the response and determines if it is valid, and 
    assuming that check is successful, returns the data.
    """
    # ping Github for information.
    response = requests.get(url, headers=headers)
    # obtain the response
    response_data = response.json()
    # check the current status code; if not 200 (received and understood) indicate an error
    if response.status_code != 200:
        print('error from url: ', url)
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data
#|---------------------------------------------------------------------------------------------|#

def get_repo_language(repo: str) -> str:
    '''
    Using a string with the named repository, this UDF inspects the elements
    of the API request and returns the programming language(s) contained therein.
    In the event of not detecting a dictionary containing a language key,
    the resultant error is indicated.
    '''
    # provides the api link with the exception of the repo name (provided in argument)
    url = f"https://api.github.com/repos/{repo}"
    # utilizes UDF above this one to garner the pinged API request
    repo_info = github_api_request(url)
    # Conditional check to validate whether the extant type is a dictionary
    if type(repo_info) is dict:
        # casts the information of the repository
        repo_info = cast(Dict, repo_info)
        # in the event the language key is not in the repository, an exception is raised
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )
#|---------------------------------------------------------------------------------------------|#

def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    """
    Using a user-provided repository title, generates the full URL to grab repo contents.
    Subsequently checks if the contents are in a list format, and if so, returns them.
    In the case where contents are not a list reponse, raises an exception. 
    """
    # provides the api link with the exception of the repo name (provided in argument)
    url = f"https://api.github.com/repos/{repo}/contents/"
    # uses the UDF from before to obtain the contents
    contents = github_api_request(url)
    # determines if the contents are in a list format and returns them if satisfied.
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    # otherwise raises an exception
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )
#|---------------------------------------------------------------------------------------------|#

def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the Github API which lists a repo's files and
    returns the URL used to download the repo's README file. This UDF accounts
    for instances of capitalization variants (as README is common), by converting to all
    lowercase during its interpretation. Returns the downloadable url if the condition
    of readme's presence is met. 
    """
    # for loop which tests whether the list contains readmes, and the download url 
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""
#|---------------------------------------------------------------------------------------------|#

def process_repo(repo: str) -> Dict[str, str]:
    """
    Receives a repository name such as "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the README contents.
    """
    # uses previous UDF to acquire the repo contents
    contents = get_repo_contents(repo)
    # obtains the download url for the freshly generated contents
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    # returns a dictionary with keys: repo, language, readme_contents
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }
#|---------------------------------------------------------------------------------------------|#

def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them.
    Returns the processed data.
    """
    # REPOS was established in the initial UDF.
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#
#|---------------------------------------------------------------------------------------------|#