from requests import get
import pandas as pd

import sklearn as sk
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, ComplementNB

random_state = 42

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 100)

def run_baseline(y_train, 
                 model_number, 
                 model_results):
    
    # establish baseline predictions for train sample
    y_pred = pd.Series([y_train.mode()[0]]).repeat(len(y_train))
    
    # get model performance metrics
    
    # create dictionaries for each metric type for the train sample and 
    # append those dictionaries to the model_results df
    dct = {'model_number': 'baseline',
           'model_type': 'baseline',
           'sample_type': 'train',
           'accuracy': sk.metrics.accuracy_score(y_train, y_pred)}
    model_results = model_results.append(dct, ignore_index=True)
    
    # reset the model_number from 'baseline' to 0
    model_number = 0
    
    return model_number, model_results

def run_decision_tree(train, validate, target,
                      model_number, model_results):
    
    # split into x and y
    x_train = train.lemmatized
    y_train = train[target]
    
    x_validate = validate.lemmatized
    y_validate = validate[target]
    
    min_max_depth = 3
    max_max_depth = 10
    
    for max_depth in range(min_max_depth, max_max_depth+1):
        
        
        
        # create classifier tree object
        tree = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
       
        #################
        #### TF-IDF #####
        #################
        
        model_number += 1
        model_type = 'decision_tree'
        feature_type = 'TF-IDF'
        
        # create the model
        tfidf = TfidfVectorizer().fit(x_train)
        x_tfidf = tfidf.transform(x_train)
        tree.fit(x_tfidf, y_train)
        
        # store info about the model
        
        ####################
        ### train sample ###
        ####################
            
        # create a dictionary containing the features and hyperparameters
        # used in this model instance
        dct = {'model_number': model_number,
               'model_type': model_type,
               'sample_type': 'train',
               'feature_type': feature_type,
               'max_depth': max_depth,
               'accuracy': tree.score(tfidf.transform(x_train), y_train)}
        # append that dictionary to the model_results dataframe
        model_results = model_results.append(dct, ignore_index=True)
        
        #######################
        ### validate sample ###
        #######################
        
        # create a dictionary containing the features and hyperparameters
        # used in this model instance
        dct = {'model_number': model_number,
               'model_type': model_type,
               'sample_type': 'validate',
               'feature_type': feature_type,
               'max_depth': max_depth,
               'accuracy': tree.score(tfidf.transform(x_validate), y_validate)}
        # append that dictionary to the model_results dataframe
        model_results = model_results.append(dct, ignore_index=True)
        
        ##############
        ### CV/BOW ###
        ##############
        
        model_number += 1
        model_type = 'decision_tree'
        feature_type = 'CV/BOW'
        
        # create the model
        cv = CountVectorizer().fit(x_train)
        x_cv = cv.transform(x_train)
        tree.fit(x_cv, y_train)
        
        # store info about the model
        
        ####################
        ### train sample ###
        ####################
            
        # create a dictionary containing the features and hyperparameters
        # used in this model instance
        dct = {'model_number': model_number,
               'model_type': model_type,
               'sample_type': 'train',
               'feature_type': feature_type,
               'max_depth': max_depth,
               'accuracy': tree.score(cv.transform(x_train), y_train)}
        # append that dictionary to the model_results dataframe
        model_results = model_results.append(dct, ignore_index=True)
        
        #######################
        ### validate sample ###
        #######################
        
        # create a dictionary containing the features and hyperparameters
        # used in this model instance
        dct = {'model_number': model_number,
               'model_type': model_type,
               'sample_type': 'validate',
               'feature_type': feature_type,
               'max_depth': max_depth,
               'accuracy': tree.score(cv.transform(x_validate), y_validate)}
        # append that dictionary to the model_results dataframe
        model_results = model_results.append(dct, ignore_index=True)

    return model_number, model_results

def run_random_forest(train, validate, target,
                      model_number, model_results):
    
    # split into x and y
    x_train = train.lemmatized
    y_train = train[target]
    
    x_validate = validate.lemmatized
    y_validate = validate[target]
    
    # set hyperparameters
    min_max_depth = 3
    max_max_depth = 6
    min_min_samples_leaf = 3
    max_min_samples_leaf = 6
    
    for max_depth in range(min_max_depth, 
                           max_max_depth+1):
        for min_samples_leaf in range(min_min_samples_leaf, 
                                      max_min_samples_leaf+1):
            
            clf = RandomForestClassifier(min_samples_leaf=min_samples_leaf,
                                         max_depth=max_depth, 
                                         random_state=random_state)
            
            ############
            ## TF-IDF ##
            ############
            
            model_number += 1
            model_type = 'random_forest'
            feature_type = 'TF-IDF'

            
            # create the model
            tfidf = TfidfVectorizer().fit(x_train)
            x_tfidf = tfidf.transform(x_train)
            clf.fit(x_tfidf, y_train)
            
            # store info about the model
            
            ####################
            ### train sample ###
            ####################
            
            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'train',
                   'feature_type': feature_type,
                   'max_depth': max_depth,
                   'min_samples_leaf': min_samples_leaf,
                   'accuracy': clf.score(tfidf.transform(x_train), y_train)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)

            #######################
            ### validate sample ###
            #######################

            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'validate',
                   'feature_type': feature_type,
                   'max_depth': max_depth,
                   'min_samples_leaf': min_samples_leaf,
                   'accuracy': clf.score(tfidf.transform(x_validate), y_validate)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)
            
            ##############
            ### CV/BOW ###
            ##############

            model_number += 1
            model_type = 'random_forest'
            feature_type = 'CV/BOW'

            # create the model
            cv = CountVectorizer().fit(x_train)
            x_cv = cv.transform(x_train)
            clf.fit(x_cv, y_train)

            # store info about the model

            ####################
            ### train sample ###
            ####################

            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'train',
                   'feature_type': feature_type,
                   'max_depth': max_depth,
                   'min_samples_leaf': min_samples_leaf,
                   'accuracy': clf.score(cv.transform(x_train), y_train)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)

            #######################
            ### validate sample ###
            #######################

            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'validate',
                   'feature_type': feature_type,
                   'max_depth': max_depth,
                   'min_samples_leaf': min_samples_leaf,
                   'accuracy': clf.score(cv.transform(x_validate), y_validate)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)
            
    return model_number, model_results
        
        
def run_naive_bayes(train, validate, target,
                    model_number, model_results):
    
    # split into x and y
    x_train = train.lemmatized
    y_train = train[target]
    
    x_validate = validate.lemmatized
    y_validate = validate[target]
    
    # set hyperparameters
    for alpha in [.1, .5, 1, 1.5, 2]:
        for classifier, model_type in zip([MultinomialNB(alpha=alpha), ComplementNB(alpha=alpha)], 
                                          ['MultinomialNB', 'ComplementNB']):

            # create the model
            clf = classifier

            ############
            ## TF-IDF ##
            ############

            model_number += 1
            model_type = model_type
            feature_type = 'TF-IDF'

            # fit the model
            tfidf = TfidfVectorizer().fit(x_train)
            x_tfidf = tfidf.transform(x_train)
            clf.fit(x_tfidf, y_train)

            # store info about the model

            ####################
            ### train sample ###
            ####################

            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'train',
                   'feature_type': feature_type,
                   'alpha': alpha,
                   'accuracy': clf.score(tfidf.transform(x_train), y_train)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)

            #######################
            ### validate sample ###
            #######################

            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'validate',
                   'feature_type': feature_type,
                   'alpha': alpha,
                   'accuracy': clf.score(tfidf.transform(x_validate), y_validate)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)

            ##############
            ### CV/BOW ###
            ##############

            model_number += 1
            model_type = model_type
            feature_type = 'CV/BOW'

            # create the model
            cv = CountVectorizer().fit(x_train)
            x_cv = cv.transform(x_train)
            clf.fit(x_cv, y_train)

            # store info about the model

            ####################
            ### train sample ###
            ####################

            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'train',
                   'feature_type': feature_type,
                   'alpha': alpha,
                   'accuracy': clf.score(cv.transform(x_train), y_train)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)

            #######################
            ### validate sample ###
            #######################

            # create a dictionary containing the features and hyperparameters
            # used in this model instance
            dct = {'model_number': model_number,
                   'model_type': model_type,
                   'sample_type': 'validate',
                   'feature_type': feature_type,
                   'alpha': alpha,
                   'accuracy': clf.score(cv.transform(x_validate), y_validate)}
            # append that dictionary to the model_results dataframe
            model_results = model_results.append(dct, ignore_index=True)
            
    return model_number, model_results

def display(model_results):
    '''
    This function takes in the model_results dataframe. This is a dataframe in tidy data format 
    containing the following information for each model created in the project:
    - model number
    - sample type
    - feature_type
    - hypterparameter values
    - accuracy (the accuracy score for the given model and sample type)
    The function returns a pivot table of those values for easy comparison of models, metrics, and samples. 
    '''
    # create a pivot table of the model_results dataframe
    # establish columns as the model_number, with index grouped by metric_type then sample_type, and values as score
    # the aggfunc uses a lambda to return each individual score without any aggregation applied
    return model_results.pivot_table(columns=['model_number'], 
                                     index=('sample_type'), 
                                     values='accuracy',
                                     aggfunc=lambda x: x)

def get_best(model_results):
    '''takes in the model_results dataframe and returns a list of the model number(s)
    that have the highest accuracy score on the validate sample.'''
    # filter for validate sample results
    validate_results = model_results[model_results.sample_type == 'validate']
    # filter for the highest accuracy score
    best_models = validate_results[validate_results.accuracy == validate_results.accuracy.max()]
    # return the associated model numbers as a list
    return list(best_models.model_number.values)

def test_model_68(train, test, target):
    '''
    recreates model #6 and return the accuracy score
    for its performance on the test sample
    '''   
    # split into x and y
    x_train = train.lemmatized
    y_train = train[target]
    x_test = test.lemmatized
    y_test = test[target]
    
    # create the model
    clf = ComplementNB(alpha=2)
    
    # preprocess features
    cv = CountVectorizer().fit(x_train)
    x_cv = cv.transform(x_train)
    
    # fit the model
    clf.fit(x_cv, y_train)
    
    # return accuracy score
    return clf.score(cv.transform(x_test), y_test)

