import requests
import json
from pprint import pprint

r = requests.get('https://api.github.com/repos/guillemborrell/thermopy/contents/')
if(r.ok):
    repoItem = json.loads(r.text or r.content)
    for file_or_folder in repoItem:
        if file_or_folder.get('name') == '.abandoned' :
            abandoned_file = file_or_folder
            break

pprint(abandoned_file)