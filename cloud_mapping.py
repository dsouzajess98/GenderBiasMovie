import pandas as pd
from pandas.core import indexing
from gender_predictor.GenderClassifier import classify_gender


def read_input_file(filename):
    data_df = pd.read_csv(filename,sep='\t', skip_blank_lines=True, index_col= False)
    return data_df

#movie_id	sentence_id	 token_id	dependent	dep_pos	 dep_ner	 governor

def get_plots_by_movie_id(data_df):
    movie_ids = data_df.movie_id.unique()  
    grouped = data_df.groupby(data_df.movie_id)

    all_movie_plots = []
    for id in movie_ids:
        sents_df = grouped.get_group(id)
        all_movie_plots.append(sents_df)
    return all_movie_plots

def get_name_and_adjective_mapping(all_movie_plots):
    name_adj_cluster_all_list = []
    for movie in all_movie_plots:
        character_adj = {}
        name_data  = movie[ movie.dep_pos == 'NNP' ]
      
        for idx,name in name_data.iterrows():
        #adjective = movie[int(name_data['governor'])]
            
            character_name = name['dependent']
            gender = classify_gender(character_name)

            if character_name not in character_adj.keys():
                character_adj[character_name] = {"adjectives":[],"gender":gender}

            governor = int(name['governor'])
            governor_df = movie[movie['token_id'] == governor]
            if governor_df['dep_pos'].values[0] == 'JJ':
                character_adj[character_name]["adjectives"].append(governor_df['dependent'].values[0])
    
        name_adj_cluster_all_list.append(character_adj) 

    return name_adj_cluster_all_list


def get_adjective_cloud(filename):
    movie_data_df = read_input_file(filename)
    all_movie_plots = get_plots_by_movie_id(movie_data_df)
    name_adj_cluster_list = get_name_and_adjective_mapping(all_movie_plots)
    print(name_adj_cluster_list)


#get_adjective_cloud("SampleDependency.txt")


#Output is the list of dictionaries mapping name of characters to the list of its corresponding adjectives 
#[{'Rohit': ['orphans'], 'Amit': []}]



