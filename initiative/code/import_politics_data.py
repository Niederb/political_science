import os
import numpy as np
import pandas as pd

"""
This is a script to merge the information of all the data files into a single
file. All the .csv files in the import_folder will be processed.
The final data will be stored in preprocessed_data.csv
Only communities will be stored that have data for all the initiative. If an
entry is missing the community will be removed. This usually happens whenever 
A list of all removed communities will be stored in remove_communities.csv
"""

def get_single_language(kanton):
    """ Returns the language given the canton abbreviation for a single canton
    """
    if (kanton == "TI"):
        return "IT"
    elif (kanton in ["FR", "VD", "NE", "JU", "GE", "VS"]):
        return "FR"
    else:
        return "DE"

def get_language(kanton):
    """ Returns the language given the canton abbreviation for a single canton
    """
    language = kanton    
    return language.apply(get_single_language)

def process_file(data_set, file_name, question_name):
    file_data = pd.read_csv(file_name, sep=';', index_col=1)
    file_data = file_data.drop('Gemeinde-Nr.', axis=1)
    #print(file_data.columns)
    #file_data.rename(columns={"Stimmberechtigte":"entitled", "Abgegebene Stimmern" : "voted", "Gueltige Stimmen" : "valid", "Ja Stimmen" : "yes"}, inplace=True)
    file_data.rename(columns={file_data.columns[0]:"entitled", file_data.columns[1] : "voted", file_data.columns[2] : "valid", file_data.columns[3] : "yes"}, inplace=True)
    file_data["yes_percent"] = pd.Series(file_data["yes"]/file_data["valid"], index=file_data.index) 
    file_data["voted_percent"] = pd.Series(file_data["voted"]/file_data["entitled"], index=file_data.index) 
    file_data.rename(columns=lambda x: question_name+"$"+x, inplace=True)
    return pd.concat([data_set, file_data], axis=1)

data_root = '../data/'
import_folder = data_root + 'preprocessed/csv/'
data_set = pd.read_csv(data_root + 'community_kanton.csv', sep=',', index_col=1)
data_set["language"] = pd.Series(get_language(data_set["Kanton"]), index=data_set.index)    

n_files = 0
file_list = []
for i in os.listdir(import_folder):
    if i.endswith(".csv"):        
        file_name = import_folder + i
        question_name = os.path.splitext(i)[0]
        file_list.append(question_name)
        print(file_name)
        data_set = process_file(data_set, file_name, question_name)
        n_files += 1

n_cols_per_question = 6
n_cols = n_files*n_cols_per_question
data_set.isnull().sum().sum()
#print('Records with NANs: %i' % sum(map(any, data_set.isnull())))
has_nan = data_set.isnull().any(axis=1)
nan_communities=data_set.ix[has_nan, 2:].isnull().sum(axis=1) / n_cols_per_question
#nan_communities = pd.DataFrame(data_set.isnull()[has_nan].sum(axis=1) index=nan_communities)
nan_communities.to_csv(data_root + 'remove_communities.csv')
data_set = data_set.dropna(how='any')
data_set.to_csv(data_root + 'preprocessed_data.csv')

data_array = data_set.ix[:, 2:].values
n_communities = np.shape(data_array)[0]