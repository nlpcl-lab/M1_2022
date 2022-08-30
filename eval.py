from beir import util, LoggingHandler
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.lexical import BM25Search as BM25

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
#retriever.k_values = [1,2,3,4,5,6,7,8,9,10,20,50,100]
retriever.k_values = [2]
logging.info("Retriever evaluation for k in: {}".format(retriever.k_values))
top_k_accuracy = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="top_k_accuracy")
print('top_k_accuracy: {}'.format(top_k_accuracy))
logging.info(print('top_k_accuracy: {}'.format(top_k_accuracy)))


#### Retrieval Example ####
query_id, scores_dict = random.choice(list(results.items()))
logging.info("Query : %s\n" % queries[query_id])

scores = sorted(scores_dict.items(), key=lambda item: item[1], reverse=True)
for rank in range(10):
    doc_id = scores[rank][0]
    logging.info("Doc %d: %s [%s] - %s\n" % (rank+1, doc_id, corpus[doc_id].get("title"), corpus[doc_id].get("text")))