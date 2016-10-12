import requests
import json
from pprint import pprint
import base64
import codecs


def base64ToString(b):
    return base64.b64decode(b)


if __name__ == '__main__':
    r = requests.get('https://api.github.com/repos/guillemborrell/thermopy/contents/')
    if(r.ok):
        repoItem = json.loads(r.text or r.content, parse_float=True)
        for file_or_folder in repoItem:
            if file_or_folder.get('name') == '.abandoned' :
                abandoned_file = file_or_folder
                break

    r = requests.get('https://api.github.com/repos/cperales/Riesgo-Reputacional-PyConES2016/contents/README.md')
    #r = requests.get('https://api.github.com/repos/guillemborrell/thermopy/contents/.abandoned')
    if(r.ok):
        repoItem = json.loads(r.text or r.content, parse_float=True)
        f = base64ToString(repoItem['content'])
        g = f.decode("utf8")
        print(f)
        print(g)
