import requests
import json
from pprint import pprint
import base64
import codecs


def base64ToString(b):
    return base64.b64decode(b)

def repos_from_user(username):
    """
    Returns a list of strings with the names of the repositories
    """
    r = requests.get('https://api.github.com/users/' + username + '/repos')
    if 'rate limit' in r.text:
        print('Rate limit exceeded')
        raise ValueError
    repoItem = json.loads(r.text or r.content, parse_float=True)
    list_of_repos = []
    for repo in repoItem:
        list_of_repos.append(repo.get('name'))
    return list_of_repos

def is_abandoned(username, repo):
    """
    Returns true if the repository is abandoned
    """
    r = requests.get('https://api.github.com/repos/' + username + '/' + repo + '/contents/')
    if(r.ok):
        repoItem = json.loads(r.text or r.content, parse_float=True)
        for file_or_folder in repoItem:
            if file_or_folder.get('name') == '.abandoned' :
                abandoned_file = file_or_folder
                return True
        return False
    else:
        if 'rate limit' in r.text:
            print('Rate limit exceeded')
        raise ValueError

def get_abandoned_info(abandoned_file):
    """
    """
    r = requests.get('https://api.github.com/repos/' + username + repo +'/contents/.abandoned')
    if(r.ok):
        repoItem = json.loads(r.text or r.content, parse_float=True)
        f = base64ToString(repoItem['content'])
        return f
        #g = f.decode("utf8")
        #print(g)

if __name__ == '__main__':
    username = 'guillemborrell'
    repositories = repos_from_user(username)

    for repo in repositories:
        if is_abandoned(username, repo):
            print(repo + ' is abandoned')
            info = get_abandoned_info(username, repo)
            print(info)
