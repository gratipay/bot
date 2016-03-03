#!/usr/bin/env python3
import re
import os
import traceback

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


class Radar(object):

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


    def find_current_tickets(self):
        return self.hit_api('get', params={'labels': 'Radar'})

    def create_ticket(self, title, body, labels):
        ticket = self.hit_api('post', json={'title': title, 'body': body, 'labels': labels})
        print("created {}".format(ticket['html_url']))

    def close_ticket(self, number):
        ticket = self.hit_api('patch', '/{}'.format(number), json={'state': 'closed'})
        print("closed {}".format(ticket['html_url']))


    def rotate(self, ticket):
        prev_title = ticket['title']
        assert re.match(r"[A-Za-z ]*Radar [0-9]+", prev_title), prev_title

        title_base, prev_radar_number = prev_title.rsplit(None, 1)
        prev_radar_number = int(prev_radar_number)

        prev_ticket_number = ticket['number']
        assert type(prev_ticket_number) is int, prev_ticket_number

        prev_link = "[&larr; Previous Radar Sweep]({}/{})\n\n------\n\n"
        prev_link = prev_link.format(self.urls['issues'], prev_ticket_number)

        next_title = "{} {}".format(title_base, prev_radar_number + 1)
        next_body = [prev_link, ''] + ticket['body'].splitlines()[4:]
        next_body = '\n'.join(next_body).strip()
        next_labels = [label['name'] for label in ticket['labels']]

        self.create_ticket(next_title, next_body, next_labels)
        self.close_ticket(prev_ticket_number)


def main(repo, username, password):
    radar = Radar(repo, username, password)
    current_tickets = radar.find_current_tickets()
    for ticket in current_tickets:
        try:
            radar.rotate(ticket)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    repo = os.environ['GITHUB_REPO']
    username = os.environ['GITHUB_USERNAME']
    password = os.environ['GITHUB_PASSWORD']
    main(repo, username, password)
