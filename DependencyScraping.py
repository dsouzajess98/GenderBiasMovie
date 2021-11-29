import os
from bs4 import BeautifulSoup
import gzip
import csv

def get_governor_data_helper(dependencies, word, word_id):
    governor_id = ""
    for d in dependencies:
        dependants = d.find_all("dependent")
        if d.find("dependent").text == word and dependants[0].get('idx') == word_id:
            governor_words = d.find_all("governor")
            governor_id = governor_words[0].get('idx')
    return governor_id


def get_dependency_data_helper(filepath, movie_id):
    output_list = []
    file_name = filepath + movie_id + ".xml.gz"
    if os.path.isfile(file_name):
    
        page = gzip.open(file_name,'r')
        soup = BeautifulSoup(page, 'html.parser')
        
        if(soup.find_all("sentence")):
            sentences = soup.find_all("sentence")

            for sent in sentences:
                sentence_id = sent.get('id')
                if sentence_id is not None:
                    tokens = sent.find_all("token")
                    basic_dependencies = sent.find_all("basic-dependencies")
                    dependencies = basic_dependencies[0].find_all("dep")

                    for t in tokens:
                        token_id = t.get('id')
                        if token_id is not None:

                            dependent = t.find("word").text
                            dep_pos = t.find("pos").text
                            dep_ner = t.find("ner").text

                            governor = get_governor_data_helper(dependencies, t.find("word").text, token_id)

                            # print(movie_id, sentence_id, token_id, dependent, dep_pos, dep_ner, governor)
                            row = [movie_id, sentence_id, token_id, dependent, dep_pos, dep_ner, governor]
                            output_list.append(row)

    return output_list

def write_csv_file(input_list, output_file):  

    fields = ["movie_id", "sentence_id", "token_id", "dependent", "dep_pos", "dep_ner", "governor"]

    with open(output_file, 'a') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(input_list)  

def get_dependency_data(file_name):
    output_list = []
    input_file = open(file_name, 'r')
    movie_ids = input_file.readlines()
    for mov_id in movie_ids:
        output_list += get_dependency_data_helper("corenlp_plot_summaries/", mov_id.strip())
    
    return output_list



def main():
    # dep_list = get_dependency_data('330')
    # dep_list = get_dependency_data('7806783')
    india_dep_list = get_dependency_data('india.txt')
    write_csv_file(india_dep_list, 'india.csv')

    # usa_dep_list = get_dependency_data('usa.txt')
    # write_csv_file(usa_dep_list, 'usa.csv')
    
      

if __name__ == "__main__":
    main()
