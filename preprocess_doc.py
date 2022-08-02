import json

json_corpus_preprocessed = {}

with open('/home/syjeong/Starlab/data/total_docs.json') as json_file:
    json_data = json.load(json_file)
    for data in json_data:
        json_title_text = {}
        
        json_title_text['title'] = json_data[data][0]
        json_title_text['text'] = json_data[data][1]

        json_corpus_preprocessed[data] = json_title_text
        #import pdb; pdb.set_trace()


with open('/home/syjeong/Starlab/data/preprocessed/total_docs.json', "w") as writer: 
    writer.write(json.dumps(json_corpus_preprocessed, indent=4) + "\n")