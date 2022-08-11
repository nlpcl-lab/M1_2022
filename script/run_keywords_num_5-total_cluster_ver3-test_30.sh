python /home/syjeong/Starlab/preprocess_query_qrel.py \
    --keywords_num 5

python /home/syjeong/Starlab/run_bm25.py \
    --query_path data/preprocessed/ver1/keywords_num/5/total_cluster_ver1_30_users_query_penguin.json \
    --qrel_path data/preprocessed/ver1/keywords_num/5/total_cluster_ver1_30_users_qrel_penguin.json \
    --index_name keywords_num_5-total_cluster_ver1-test_30
