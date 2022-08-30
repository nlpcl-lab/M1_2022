from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.lexical import BM25Search as BM25
from typing import Type, List, Dict, Union, Tuple


import pathlib, os, random, json, argparse
import logging
import warnings

warnings.filterwarnings(action='ignore')

parser = argparse.ArgumentParser()
parser.add_argument("--corpus_path", default="/home/syjeong/Starlab/data/preprocessed/total_docs.json", type=str, help="")
parser.add_argument("--query_path", default='data/preprocessed/ver3/keywords_num/10/total_cluster_ver3_30_users_query_penguin.json', type=str, help="")
parser.add_argument("--qrel_path", default='data/preprocessed/ver3/keywords_num/10/total_cluster_ver3_30_users_qrel_penguin.json', type=str, help="")
parser.add_argument("--index_name", default='keywords_num_10-total_cluster_ver3-test_30', type=str, help="")

args = parser.parse_args()

#### Just some code to print debug information to stdout
logging.basicConfig(
                    filename='outputs/'+args.index_name+'.log', # 
                    filemode='w',
                    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
                    datefmt="%m/%d/%Y %H:%M:%S",
                    level=logging.INFO
                )


def calculate_top_k_accuracy(
        qrels: Dict[str, Dict[str, int]], 
        results: Dict[str, Dict[str, float]], 
        k_values: List[int]) -> Tuple[Dict[str, float]]:
    
    top_k_acc = {}
    
    for k in k_values:
        top_k_acc[f"Accuracy@{k}"] = 0.0
    
    k_max, top_hits = max(k_values), {}
    logging.info("\n")
    
    for query_id, doc_scores in results.items():
        top_hits[query_id] = [item[0] for item in sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)[0:k_max]]
    
    for query_id in top_hits:
        query_relevant_docs = set([doc_id for doc_id in qrels[query_id] if qrels[query_id][doc_id] > 0])
        for k in k_values:
            for relevant_doc_id in query_relevant_docs:
                if relevant_doc_id in top_hits[query_id][0:k]:
                    top_k_acc[f"Accuracy@{k}"] += 1.0
                    break

    for k in k_values:
        top_k_acc[f"Accuracy@{k}"] = round(top_k_acc[f"Accuracy@{k}"]/len(qrels), 5)
        logging.info("Accuracy@{}: {:.4f}".format(k, top_k_acc[f"Accuracy@{k}"]))

    return top_k_acc

#### /print debug information to stdout

#### load dataset
with open(args.corpus_path) as json_file:
    corpus = json.load(json_file)

with open(args.query_path) as json_file:
    queries = json.load(json_file)

with open(args.qrel_path) as json_file:
    qrels = json.load(json_file)

#### Lexical Retrieval using Bm25 (Elasticsearch) ####
#### Provide a hostname (localhost) to connect to ES instance
#### Define a new index name or use an already existing one.
#### We use default ES settings for retrieval
#### https://www.elastic.co/

hostname = "localhost" #localhost
index_name = args.index_name # scifact

#### Intialize #### 
# (1) True - Delete existing index and re-index all documents from scratch 
# (2) False - Load existing index
initialize = True # False

#### Sharding ####
# (1) For datasets with small corpus (datasets ~ < 5k docs) => limit shards = 1 
number_of_shards = 1
model = BM25(index_name=index_name, hostname=hostname, initialize=initialize, number_of_shards=number_of_shards)

# (2) For datasets with big corpus ==> keep default configuration
# model = BM25(index_name=index_name, hostname=hostname, initialize=initialize)
retriever = EvaluateRetrieval(model)

#### Retrieve dense results (format of results is identical to qrels)
results = retriever.retrieve(corpus, queries)

#### Evaluate your retrieval using NDCG@k, MAP@K ...
retriever.k_values = [2]
logging.info("Retriever evaluation for k in: {}".format(retriever.k_values))
top_k_accuracy = calculate_top_k_accuracy(qrels, results, retriever.k_values)
print('top_k_accuracy: {}'.format(top_k_accuracy))
logging.info(print('top_k_accuracy: {}'.format(top_k_accuracy)))


#### Retrieval Example ####
query_id, scores_dict = random.choice(list(results.items()))
logging.info("Query : %s\n" % queries[query_id])

scores = sorted(scores_dict.items(), key=lambda item: item[1], reverse=True)
for rank in range(10):
    doc_id = scores[rank][0]
    logging.info("Doc %d: %s [%s] - %s\n" % (rank+1, doc_id, corpus[doc_id].get("title"), corpus[doc_id].get("text")))



