import json, argparse
import random
from collections import Counter
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument("--valid_proportaion", default=0.7, type=float, help="")
parser.add_argument("--keywords_num", default=5, type=int, help="")
args = parser.parse_args()

def make_query_qrel_for_each_cluster(cluster_num):
    json_preprocessed_queries = {}

    with open('/home/syjeong/Starlab/data/ver1/'+str(cluster_num)+'_cluster_ver1_users_penguin.json') as json_file:
        json_data = json.load(json_file)
        #import pdb; pdb.set_trace()

        # random shuffle
        random.seed(42)
        lst_total_user_keys = list(json_data.keys())
        random.shuffle(lst_total_user_keys)

        # split into 7:3
        idx_data_70 = int(len(json_data)*args.valid_proportaion)
        lst_70_user_keys = lst_total_user_keys[:idx_data_70]
        lst_30_user_keys = lst_total_user_keys[idx_data_70:]


        # sort by frequency for 70% of data (validation)
        lst_70_user_likes = []
        for user_key in tqdm(lst_70_user_keys):

            likes = json_data[user_key]['likes']
            lst_likes = list(likes.keys())
            lst_70_user_likes = lst_70_user_likes + (lst_likes)

        counter = Counter(lst_70_user_likes)
        
        # most common like keywords list
        lst_sorted_freq_70_user_likes = [i[0] for i in counter.most_common(n=args.keywords_num)]
        str_sorted_freq_70_user_likes = ', '.join(lst_sorted_freq_70_user_likes)
        
        # preprocess test query & qrel for rest of the 30% users for current cluster (test), using the frequent like keywords from 70% users (validation)
        json_query_preprocessed = {}
        json_qrel_preprocessed = {}
        for user_key in tqdm(lst_30_user_keys):

            # preprocess query for current cluster
            likes = json_data[user_key]['likes']
            lst_likes = list(likes.keys())
            lst_likes_with_community_likes = lst_likes + lst_sorted_freq_70_user_likes
            str_likes = ', '.join(lst_likes_with_community_likes)

            json_query_preprocessed[user_key] = str_likes

            # preprocess qrel for current cluster
            lst_likes_doc = [str(i) for i in json_data[user_key]['likes_doc']]

            # (TODO): 관련 있는 거는 1, 관련 없는 거는 안 써도 되는건지 확인하기..
            
            dict_like_doc = {}
            for like_doc in lst_likes_doc:
                dict_like_doc[like_doc] = 1

            json_qrel_preprocessed[user_key] = dict_like_doc

    with open('/home/syjeong/Starlab/data/preprocessed/ver1/keywords_num/'+str(args.keywords_num)+'/'+str(cluster_num)+'_cluster_ver1_30_users_query_penguin.json', "w") as writer: 
        writer.write(json.dumps(json_query_preprocessed, indent=4) + "\n")

    with open('/home/syjeong/Starlab/data/preprocessed/ver1/keywords_num/'+str(args.keywords_num)+'/'+str(cluster_num)+'_cluster_ver1_30_users_qrel_penguin.json', "w") as writer: 
        writer.write(json.dumps(json_qrel_preprocessed, indent=4) + "\n")

    return json_query_preprocessed, json_qrel_preprocessed, str_sorted_freq_70_user_likes



total_cluster_json_query_preprocessed = {}
total_cluster_json_qrel_preprocessed = {}
for i in range(0,10):
    i_cluster_json_query_preprocessed, i_cluster_json_qrel_preprocessed, cluster_like_keywords = make_query_qrel_for_each_cluster(i)
    
    # merge query for each cluster
    # if user (key) exists in both clusters, then concat two queries (value)
    for k, v in i_cluster_json_query_preprocessed.items():
        total_cluster_json_query_preprocessed[k] = total_cluster_json_query_preprocessed[k] + ' , ' + cluster_like_keywords if k in total_cluster_json_query_preprocessed else v
        
        # if k in total_cluster_json_query_preprocessed:
        #     #import pdb; pdb.set_trace()
        #     total_cluster_json_query_preprocessed[k] = total_cluster_json_query_preprocessed[k] + ' , ' + cluster_like_keywords
        # else:
        #     total_cluster_json_query_preprocessed[k] = v

    # merge qrel for each cluster
    # even if user (key) exists in both clusters, qrels are same
    # (TODO): 위의 이유로 total_cluster_json_qrel_preprocessed[k] = v 로 해도 되는지 확인..?
    for k, v in i_cluster_json_qrel_preprocessed.items():
        total_cluster_json_qrel_preprocessed[k] = {**total_cluster_json_qrel_preprocessed[k], **v} if k in total_cluster_json_qrel_preprocessed else v
        
        # if k in total_cluster_json_qrel_preprocessed:
        #     import pdb; pdb.set_trace()
        #     total_cluster_json_qrel_preprocessed[k] = {**total_cluster_json_qrel_preprocessed[k], **v}
        # else:
        #     total_cluster_json_qrel_preprocessed[k] = v

with open('/home/syjeong/Starlab/data/preprocessed/ver1/keywords_num/'+str(args.keywords_num)+'/'+'total_cluster_ver1_30_users_query_penguin.json', "w") as writer: 
    writer.write(json.dumps(total_cluster_json_query_preprocessed, indent=4) + "\n")

with open('/home/syjeong/Starlab/data/preprocessed/ver1/keywords_num/'+str(args.keywords_num)+'/'+'total_cluster_ver1_30_users_qrel_penguin.json', "w") as writer: 
    writer.write(json.dumps(total_cluster_json_qrel_preprocessed, indent=4) + "\n")