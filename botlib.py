import functools
import os

import requests


class APIError(Exception):

    def __init__(self, code, body):
        Exception.__init__(self)
        self.code = code
        self.reason = body.splitlines() and body.splitlines()[-1] or ''
        self.body = body

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<APIError {}: {}>'.format(self.code, self.reason)


class Issues(object):

    def __init__(self, repo, username, password):
        self.urls = { 'issues': 'https://github.com/{}/issues'.format(repo)
                    , 'api': 'https://api.github.com/repos/{}/issues'.format(repo)
                     }
        self.session = requests.Session()
        self.session.auth = (username, password)


    def hit_api(self, method, path_info='', params=None, json=None):
        assert method in ('get', 'post', 'patch'), method
        call = getattr(self.session, method)
        response = call(self.urls['api'] + path_info, params=params, json=json)
        if response.status_code not in (200, 201):
            raise APIError(response.status_code, response.text)
        return response.json()


def main(main):
    repo = os.environ['GITHUB_REPO']
    username = os.environ['GITHUB_USERNAME']
    password = os.environ['GITHUB_PASSWORD']
    return functools.partial(main, repo, username, password)
