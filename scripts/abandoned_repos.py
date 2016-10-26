import requests
import json
import io
import base64


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

def get_abandoned_info(username, repo):
    """
    """
    r = requests.get('https://api.github.com/repos/' + username + '/' + repo +'/contents/.abandoned')
    if(r.ok):
        repoItem = json.loads(r.text or r.content, parse_float=True)
        f = base64ToString(repoItem['content'])
        text = f.split('\n')
        final_text = ''
        for line in text:
            final_text += line
            final_text += """
"""
        return final_text

        # # Another way, more obscure
        # g = io.StringIO(f.decode('utf-8'))
        # for b in g.readlines():
        #     print(b)

if __name__ == '__main__':
    username = 'cperales'
    repositories = repos_from_user(username)

    for repo in repositories:
        if is_abandoned(username, repo):
            print(repo + ' is abandoned:')
            info = get_abandoned_info(username, repo)
            print(info)
