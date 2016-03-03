#!/usr/bin/env python3
import os, sys; sys.path.insert(0, os.path.dirname(__file__))

import re
import traceback

import botlib


class Radar(botlib.Issues):

    def find_current_tickets(self):
        return self.hit_api('get', params={'labels': 'Radar'})

    def create_ticket(self, title, body, labels):
        ticket = self.hit_api('post', json={'title': title, 'body': body, 'labels': labels})
        print("created {}".format(ticket['html_url']))

    def close_ticket(self, number):
        ticket = self.hit_api('patch', '/{}'.format(number), json={'state': 'closed'})
        print("closed {}".format(ticket['html_url']))


    def rotate(self, previous):
        prev_title = previous['title']
        assert re.match(r"[A-Za-z ]*Radar [0-9]+", prev_title), prev_title

        prev_ticket_number = previous['number']
        assert type(prev_ticket_number) is int, prev_ticket_number

        prev_link = "[&larr; {}]({}/{})\n\n------\n\n"
        prev_link = prev_link.format(prev_title, self.urls['issues'], prev_ticket_number)

        title_base, prev_radar_number = prev_title.rsplit(None, 1)
        prev_radar_number = int(prev_radar_number)

        next_title = "{} {}".format(title_base, prev_radar_number + 1)
        next_body = [prev_link, ''] + previous['body'].splitlines()[4:]
        next_body = '\n'.join(next_body).strip()
        next_labels = [label['name'] for label in previous['labels']]

        self.create_ticket(next_title, next_body, next_labels)
        self.close_ticket(prev_ticket_number)


@botlib.main
def main(repo, username, password):
    radar = Radar(repo, username, password)
    current_tickets = radar.find_current_tickets()
    for ticket in current_tickets:
        try:
            radar.rotate(ticket)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    main()
