import os
import sys
import json
from argparse import ArgumentParser

# Written by Josh Spicer <joshspicer.com>
#            Feb 16, 2019

# Requires a facebook messenger (json) export file
# https://www.facebook.com/dyi

modesString = '''

MOST_POPULAR: Counts how the total reacts each person in a group chat has received.

COUNT: Counts how many messages occur in a given timeframe.

'''

class MessengerParse:

    def __init__(self, input='', mode="COUNT"):
        self.input = input
        self.parser = ArgumentParser()
        self.__version__ = 0.1
        self.mode = mode

        # "private" variables
        self.data = []
        self.participants = []

     # Declare cli arguments here
    def parse_args(self):
        """Parse"""
        self.parser.description = 'Messenger Bulk Data Parsing Tool'
        self.parser.add_argument('input', help="json messenger archive file")
        self.parser.add_argument('--mode', help="Specify the mode to operate in. DEFAULT: MOST_POPULAR | Options: {0}".format(modesString))
        self.args = self.parser.parse_args()

        # Set all args here to class variables
        self.input = self.args.input
        self.mode = self.args.mode

    # Does some basic setup
    def setup_generic(self):
        file = open(self.input, 'r')
        self.data = json.loads(file.read())
        # print(self.data)

        # Get a dictionary of participants
        tmp = self.data['participants']
        for person in tmp:
           self.participants.append(person['name'])

    def run(self):
        if self.mode == "COUNT":
            return self.countInTimeFrame(1549972846000,1550059246000)
        elif self.mode == "MOST_POPULAR":
            return self.countMostPopularPerson()
        # ...more...
        else:
            return "Please supply a mode!"
            
    def handleCLI(self):
        self.parse_args()
        self.setup_generic()
        return self.run()

    ## ==================== WORKERS ====================== ##
    def countInTimeFrame(self, start, end):
        msgs = self.data['messages']
        count = 0
        for m in msgs:
            if m['timestamp_ms'] > start and  m['timestamp_ms'] < end:
                count = count + 1

        return count

    # counts the total number of reacts a person has gotten in the group chat.
    # Returns a list with "most popular" person at the top.
    def countMostPopularPerson(self):
        # Gen a dictionary with participants name
        popularityDict = {}
        for person in self.participants:
            popularityDict[person] = 0
        # Go though every message, and simple count the reacts on the message.
        msgs = self.data['messages']
        for m in msgs:
            sender = m['sender_name']
            count = 0
            if 'reactions' in m:
                for r in m['reactions']:
                    count = count + 1
            popularityDict[sender] = popularityDict[sender] + count

        return sorted(popularityDict.items(), key=lambda x: x[1], reverse=True)



     ## =================================================== ##




if __name__ == '__main__':
    m = MessengerParse()
    r = m.handleCLI()
    print(r)
