import json


with open('langListTemp.json', 'r') as file:
    data = json.load(file)

    vlist = {}
    for p in data:
        print(p['Name'])

        lang = {p['Name'] : {"langName": p['Value.langName'], "langCode" : p['Value.langCode'], "gender": p['Value.gender'], "sample": p['Value.sammple']}}
        vlist.update(lang)
    
    with open('languages.json', 'w') as outfile:
        json.dump(vlist, outfile)
