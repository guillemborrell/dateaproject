import requests
import json
from pprint import pprint
import io
import base64


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b)


if __name__ == '__main__':
    r = requests.get('https://api.github.com/repos/guillemborrell/thermopy/contents/')
    if(r.ok):
        repoItem = json.loads(r.text or r.content, parse_float=True)
        for file_or_folder in repoItem:
            if file_or_folder.get('name') == '.abandoned' :
                abandoned_file = file_or_folder
            elif file_or_folder.get('name') == 'readme.md':
                # pprint(file_or_folder)
                pass

    r = requests.get('https://api.github.com/repos/guillemborrell/thermopy/contents/readme.md')
    if(r.ok):
        repoItem = json.loads(r.text or r.content, parse_float=True)
        for field in repoItem.keys():
            if field == 'content':
                print(type(repoItem[field]))
                f = base64ToString(repoItem[field])
                g = io.BytesIO(f)
                print(g)

    # pprint(abandoned_file)
