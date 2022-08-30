python /home/syjeong/Starlab/preprocess_query_qrel.py \
    --keywords_num 20

python /home/syjeong/Starlab/run_bm25.py \
    --query_path data/preprocessed/ver3/keywords_num/20/total_cluster_ver3_30_users_query_penguin.json \
    --qrel_path data/preprocessed/ver3/keywords_num/20/total_cluster_ver3_30_users_qrel_penguin.json \
    --index_name keywords_num_20-total_cluster_ver3-test_30
