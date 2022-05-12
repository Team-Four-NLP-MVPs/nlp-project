# Predicting Repository Languages

![github_wordcloud](https://user-images.githubusercontent.com/69991789/127923505-65a4e277-e414-401a-a6e1-eff346135647.png)

## **See our completed presentation [here](https://docs.google.com/presentation/d/1RSblufGvC3jnTIidLAmpIXq9pnMHEzX0/edit?usp=sharing&ouid=113732050903451976581&rtpof=true&sd=true)**

## Project Goals:
- Can we successfully predict a repository's coding languge based off the readme contents?
- What readme contents contribute to the prediction of a repository's coding language?


## Project Goals/Description
The goal of this project is to predict the programming language of each repository by scraping the repository's README file contents. This project was initiated by utilizing web scraping techniques to scrape README files from various GitHub repositories. After acquiring and preparing our data, our team conducted natural language processing exploration methods such as word clouds, bigrams and trigrams. We employed multiclass classification methods to create multiple machine learning models. The end goal was to create an NLP model that accurately predicted the programming language used in a github repository based on the words and word combinations found in the readme files.

### Project Outline:
    
- Acquisiton of data:
    - Search for repositories on git hub with "customer" as a commonality.
    - Conduct web scraping of said repositories' readme contents.
- Prepare and clean data:
    - Remove repositories in languages other than english
    - Drop nulls
    - Lowercase all text
    - Remove stopwords (including customer, customers, 1, 2, and i)
    - Tokenize the data
    - Stem and Lemmatize
    - Narrow data down to repo's top four languages (java, javascript, php and jupyter)
- Explore data:
    - Explore word clouds for top 4 languages
    - How often are words used?
        - Analyze top 20 words for each language
    - Utilize bar graphs, bigrams and trigrams for top 4 languages
    - Analyze bigram and trigram word clouds for top 4 languages
- Modeling:
    - Created baseline model based off most common language (PHP)
    - Make multiple competitive models
    - Use cleaned, stemmed and lemmatized data on models
    - Pick best performing model to move forward with.
    - Test the top model on unseen test data set
    - Conclude results
    
### Target variable
- Language

## Findings:
## Data Wrangle:
- Web scraped respository README files that had the word "customer" in them
- Filtered out the scraped content by removing non-english repos
- Normalized, tokenized, stemmed and lemmatized the content for NLP
- Split data into train, validate and test set
### Explore:
- PHP is the most commonly used coding language
- Some words were key identifiers to their language, such as "magento" for PHP and "model" for jupyter
- Bigrams and Trigrams have variable phrases for each language and no major commonality across the different languages.
- Java and JavaScript had no unique identifiers in their top words to their specific language
    
### Modeling:
- Baseline Model:
    - Using language mode (PHP being the most common) to create baseline.
    - Accuracy is 38% on unseen data.
- Models created on cleaned, stemmed and lemmatized data:
    - Support Vector Classification (SVC)
    - K-Nearest Neighbor (KNN)
    - Naive Bayes
    - Decision Tree
    - Random Forest
    - Logistic Regression
- Best Model:
    - SVC (on lemmatized data)
- Model testing:
    - Train Dataset
        - 100% accuracy
    - Validate Dataset (unseen)
        - 85% accuracy
- Performance:
    - Test Dataset (unseen)
        - 82% accuracy


## Replicate My Project
### tools/libraries:
    1. python
    2. pandas
    3. scipy
    4. sci-kit learn
    5. numpy
    6. matplotlib.pyplot
    7. seaborn
    8. NLTK
    9. BeautifulSoup
* Steps to recreate
    1. If you wish to recreate this project:

    - Read the README.md
    - Download the data2.json file
    - Download the prepare.py, explore.py, model.py and project_final_notebook.ipynb files into your working directory, or clone this repository
    - Ensure your json file is named appropriately (data2.json)
    - Run the project_final_notebook.ipynb notebook


------------


## Data Dictionary

#### Target
Name | Description | Type
:---: | :---: | :---:
language | The repository's respective programming language | object
#### Features
Name | Description | Type
:---: | :---: | :---:
repo | The name of the specific repository | object
readme_contents | The contents of readme file scraped from that repo | object
cleaned | The readme contents with stopwords removed, text normalized and tokenized | object
stemmed | The cleaned data stemmed | object
lemmatized | The cleaned data lemmatized | object



## Recommendations/With More Time:
1. We would add in varying repo languages to see if we could increase the model's drop off on validate set.
2. Adding in more Java and JavaScript readme files specifically may help model performance since they are the lowest amount of repos we have.
