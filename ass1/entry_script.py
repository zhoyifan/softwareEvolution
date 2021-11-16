import sys
import math
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('book')
#nltk.download('gutenberg') 
from nltk.corpus import stopwords
from nltk.book import *

# Global variables
pattern = r"""(?x) 
        (?:[a-z]\.)+      
        |\$?\d+(?:\.\d+)?%?    
        |\w+(?:[-']\w+)*      
        """
tokenizer = nltk.tokenize.RegexpTokenizer(pattern)  # Regular expression tokenizer
stop_words = set(stopwords.words('english'))  # Stop-words glossary
poster2_stemmer = nltk.stem.snowball.EnglishStemmer()  # Poster2 stemmer


def write_output_file(output, undetected_spurious, filename):
    """
    Writes a dummy output file using the python csv writer, update this
    to accept as parameter the found trace links.
    """
    path = "/output/" + str(filename) + ".csv"
    path_undetected = "/output/" + str(filename) + "_undetected" + ".csv"
    path_spurious = "/output/" + str(filename) + "_spurious" + ".csv"
    # path = r".\output" + "\\" + str(filename) + ".csv"
    # path_undetected = r".\output" + "\\" + str(filename) + "_undetected" + ".csv"
    # path_spurious = r".\output" + "\\" + str(filename) + "_spurious" + ".csv"

    # output file generation
    output.to_csv(path, index=False)

    # undetected trace-links file generation
    set_to_df(undetected_spurious[1]).to_csv(path_undetected, index=False)

    # spurious trace-links file generation
    set_to_df(undetected_spurious[2]).to_csv(path_spurious, index=False)



def pre_processing(data_frame):
    """
    :param data_frame: the original dataset with requirement/use-case id and the content.
    :return dict: a dictionary with key(requirement id) and value(Frequency distribution of tokens)
    """
    dict={} # To store requirement id and processed tokens.
    for index,record in data_frame.iterrows():
        raw_content = str(record["text"]).lower()
        # Parsing and tokenizing using regular expression tokenizer.
        tokens = tokenizer.tokenize(raw_content)
        # Stop-words Removal.
        tokens_removal = [i for i in tokens if i not in stop_words]
        # Stemming.
        stemmed_tokens = [poster2_stemmer.stem(i) for i in tokens_removal]
        # Frequency Distribution for a requirement.
        freq_dist=FreqDist(stemmed_tokens)
        dict[record["id"]] = freq_dist
    return dict


def idf_calculation(high_dict, low_dict):
    # Calculate the number of requirements containing a specific word
    num_of_req = {}
    for dict in [high_dict,low_dict]:
        for req_id, freq_dist in dict.items():
            for token in freq_dist:
                if token in num_of_req:
                    num_of_req[token]+=1
                else:
                    num_of_req[token]=1
    # Calculate the idf value for all tokens
    idf = {}
    for token in num_of_req:
        idf[token]=math.log2((len(high_dict)+len(low_dict))/num_of_req[token])
    return idf


def vector_representation(dict, idf):
    """
    :param dict: The dictionary for requirement documents with keys(requirment id) and values(frequency distribution)
    :param idf: The dictionary storing idf value for mater vocabulary
    :return: a dictionary with keys(requirement id) and values(vector representation)
    """
    tf_idf={}
    for req_id, freq_dist in dict.items():
        tf_idf[req_id]={}
        for token in freq_dist:
            freq=freq_dist[token]
            tf_idf[req_id][token]=freq*idf[token]
    return tf_idf


def similarity_matrix(vec_high, vec_low):
    """
    :param vec_high: vector representation for high-level requirement document
    :param vec_low: vector representation for low-level requirement document
    :return: similarity matrix
    """
    sim_mat = pd.DataFrame(index=list(vec_high.keys()), columns=list(vec_low.keys()))
    for h_req_id, h_vector in vec_high.items():
        for l_req_id, l_vector in vec_low.items():
            sim_mat.loc[h_req_id,l_req_id] = get_similarity(h_vector, l_vector)
    return sim_mat


def get_similarity(h, l):
    # calculate the cosine of an angle between vector h and l
    x_pow2 = 0
    y_pow2 = 0
    xy = 0
    for h_token, h_tf_idf in h.items():
        x_pow2 += h_tf_idf * h_tf_idf
    for l_token, l_tf_idf in l.items():
        y_pow2 += l_tf_idf * l_tf_idf
        if l_token in h:
            xy += l_tf_idf * h[l_token]
        else:
            xy += 0
    return xy/(math.sqrt(x_pow2) * math.sqrt(y_pow2))


def link_generation(mode, sim_mat):
    rows=[]
    threshold = 0
    upper_bound = 100
    if mode == 0:
        threshold = 0.00000000001
    elif mode == 1:
        threshold = 0.25
    for h_req_id, row in sim_mat.iterrows():
        l_req_list = []
        if mode == 2:
            threshold = 0.67 * row.max()
        if mode == 3:
            threshold = 0.67 * row.max()
            upper_bound = 2
        row2 = row.sort_values(axis = 0, ascending=False)
        for l_req_id, sim in row2.iteritems():
            if sim >= threshold:
                l_req_list.append(l_req_id)
            if len(l_req_list) >= upper_bound:
                break
        new_row = pd.Series(index=["id", "links"])
        new_row["id"] = h_req_id
        if len(l_req_list) > 0:
            new_row["links"] = ','.join([str(i) for i in l_req_list])
        rows.append(new_row)
    output = pd.concat(rows, axis=1).transpose()
    return output


def extract_link_set(df_links):
    link_set = set()
    for h_req_id, row in df_links.iterrows():
        if type(row["links"]) == str :
            l_req_ids = row["links"].split(",")
            for l_req_id in l_req_ids:
                link_set.add(row["id"]+"-"+l_req_id)
    return link_set


def evaluation(tool_output, manual_links, total_num, identifier):
    tool_links = extract_link_set(tool_output)
    true_positive = len(manual_links.intersection(tool_links))  # upper left
    false_negative = len(manual_links) - true_positive  # upper right
    false_positive = len(tool_links) - true_positive  # bottom left
    true_negative = total_num - true_positive - false_negative - false_positive # bottom right
    confusion_mat = pd.DataFrame([[true_positive, false_negative], [false_positive, true_negative]]
                           , index=["trace-link identified manually", "trace-link not-identified manually"]
                           , columns=["trace-link predicted by the tool", "trace-link not predicted by the tool"])
    print("The confusion matrix for ", identifier, " is: \n", confusion_mat, "\n")
    # precision, recall, F-measure
    recall = true_positive / (true_positive + false_negative)
    precision = true_positive / (true_positive + false_positive)
    f_measure = 2 * precision * recall / (precision + recall)
    print("recall: ", recall)
    print("precision: ", precision)
    print("F-measure: ", f_measure)

    # output files of false positive and false negative
    tru_pos = manual_links.intersection(tool_links)
    fal_neg = manual_links.difference(tru_pos)
    fal_pos = tool_links.difference(tru_pos)
    return {1: fal_neg, 2: fal_pos}


def set_to_df(link_set):
    link_dict={}
    for i in link_set:
        link=i.split('-')
        if link[0] in link_dict:
            link_dict[link[0]]+=','+link[1]
        else:
            link_dict[link[0]]=link[1]
    return pd.DataFrame(link_dict.items(), columns=['id','links'])


if __name__ == "__main__":
    '''
    Entry point for the script
    '''
    if len(sys.argv) < 2:
        print("Please provide an argument to indicate which matcher should be used")
        exit(1)

    match_type = 0

    try:
        match_type = int(sys.argv[1])
    except ValueError as e:
        print("Match type provided is not a valid number")
        exit(1)

    print(f"Hello world, running with matchtype {match_type}!")
    print("the system argument are:", sys.argv[0] + "," + sys.argv[1])

    # Read input high-level and low-level requirements
    df_high = pd.read_csv("/input/high.csv")
    df_low = pd.read_csv("/input/low.csv")
    df_links = pd.read_csv("/input/links.csv")
    # df_high = pd.read_csv(r".\dataset-2\high.csv")
    # df_low = pd.read_csv(r".\dataset-2\low.csv")
    # df_links = pd.read_csv(r".\dataset-2\links.csv")

    # Check for duplicate id and content
    print("high.csv has duplicated id?", df_high['id'].duplicated().any())
    print("high.csv has duplicated text?", df_high['text'].duplicated().any())
    print("low.csv has duplicated id?", df_low['id'].duplicated().any())
    print("low.csv has duplicated text?", df_low['text'].duplicated().any())

    # Pre-Processing data
    dict_high = pre_processing(df_high)
    dict_low = pre_processing(df_low)

    # Vector representation
    idf = idf_calculation(dict_high,dict_low)
    vec_high = vector_representation(dict_high, idf)
    vec_low = vector_representation(dict_low, idf)

    # Get similarity matrix
    sim_mat = similarity_matrix(vec_high, vec_low)

    manual_link_set = extract_link_set(df_links)
    num = len(dict_high) * len(dict_low)

    # match type and generate links
    if match_type == 0:
        # implement all baseline technique
        no_filtering = link_generation(0, sim_mat)
        at_least_0_25 = link_generation(1, sim_mat)
        at_least_0_67_max = link_generation(2, sim_mat)
        filter_with_upper_bound = link_generation(3, sim_mat)

        # Evaluation
        undetected_spurious1 = evaluation(no_filtering, manual_link_set, num, "no filtering")
        undetected_spurious2 = evaluation(at_least_0_25, manual_link_set, num, "at least 0.25")
        undetected_spurious3 = evaluation(at_least_0_67_max, manual_link_set, num, "at least 0.67 max")
        undetected_spurious4 = evaluation(filter_with_upper_bound, manual_link_set, num, "at least 0.67 max with upper bound")

        # File generation
        write_output_file(no_filtering, undetected_spurious1, "no_filtering")
        write_output_file(at_least_0_25, undetected_spurious2, "at_least_0_25")
        write_output_file(at_least_0_67_max, undetected_spurious3, "at_least_0_67_max")
        write_output_file(filter_with_upper_bound, undetected_spurious4, "0_67_max_with_UB")
    elif match_type == 1:
        # >0 filtering
        no_filtering = link_generation(0, sim_mat)
        undetected_spurious1 = evaluation(no_filtering, manual_link_set, num, "no filtering")
        write_output_file(no_filtering, undetected_spurious1, "no_filtering")
    elif match_type == 2:
        # >=0.25 filtering
        at_least_0_25 = link_generation(1, sim_mat)
        undetected_spurious2 = evaluation(at_least_0_25, manual_link_set, num, "at least 0.25")
        write_output_file(at_least_0_25, undetected_spurious2, "at_least_0_25")
    elif match_type == 3:
        # >=0.67max filtering
        at_least_0_67_max = link_generation(2, sim_mat)
        undetected_spurious3 = evaluation(at_least_0_67_max, manual_link_set, num, "at least 0.67 max")
        write_output_file(at_least_0_67_max, undetected_spurious3, "at_least_0_67_max")
    elif match_type == 4:
        # >=0.67max & UB = 2
        filter_with_upper_bound = link_generation(3, sim_mat)
        undetected_spurious4 = evaluation(filter_with_upper_bound, manual_link_set, num, "at least 0.67 max with upper bound")
        write_output_file(filter_with_upper_bound, undetected_spurious4, "0_67_max_with_UB")
    else:
        print("Wrong mode selection! Please try again and enter the correct mode number!")
