import json

sample_json = []
sample_json_dict={}
with open('/home/syjeong/Starlab/data/ver1/0_cluster_ver1_users_penguin_.json') as json_file:
    json_data = json.load(json_file)
    
    for i, data in enumerate(json_data):
        import pdb; pdb.set_trace()
        if i < 5: #11077
            sample_json.append(data)
        else:
            sample_json_dict["data"] = sample_json
            break

with open("/home/syjeong/Starlab/data/preprocessed/temp/ver1/0_cluster_ver1_users_penguin.json", "w") as json_file: 
    json.dump(sample_json_dict, json_file)
