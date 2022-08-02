import json

with open('/home/syjeong/Starlab/data/ver1/0_cluster_ver1_docs_penguin.json') as json_file:
    json_data = json.load(json_file)

with open('/home/syjeong/Starlab/data/ver1/0_cluster_ver1_docs_penguin_.json', "w") as writer: 
    writer.write(json.dumps(json_data, indent=4) + "\n")
