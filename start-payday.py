#!/usr/bin/env python3
import os, sys; sys.path.insert(0, os.path.dirname(__file__))

import re
import botlib


class Paydays(botlib.Issues):

    def find_previous(self):
        return self.hit_api('get', params={'labels': 'Payday'})[0]

    def get_crew(self):
        return ('@whit537', '@clone1018', '@rohitpaulk')

    def create_next(self, previous):
        prev_title = previous['title']
        assert re.match(r"Payday [0-9]+", prev_title), prev_title

        prev_ticket_number = previous['number']
        assert type(prev_ticket_number) is int, prev_ticket_number

        prev_link = '[&larr; {}]({}/{})'
        prev_link = prev_link.format(prev_title, self.urls['issues'], previous['number'])

        pilot, copilot, first_mate = self.get_crew()

        n = int(prev_title.split()[-1])
        next_title = 'Payday {}'.format(n + 1)
        next_body = '{}\n\n-------\n\nThis month: {} ({})\n\nNext month: {} ({})'
        next_body = next_body.format(prev_link, pilot, copilot, copilot, first_mate)

        payload = {'title': next_title, 'body': next_body, 'labels': ['Payday']}
        ticket = self.hit_api('post', json=payload)
        print("created {}".format(ticket['html_url']))


@botlib.main
def main(repo, username, password):
    paydays = Paydays(repo, username, password)
    previous = paydays.find_previous()
    paydays.create_next(previous)


if __name__ == '__main__':
    main()
