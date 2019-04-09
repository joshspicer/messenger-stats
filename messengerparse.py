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

COUNT: Counts how many messages occur in a given timeframe. (work in progress)

MOST_GIVING: Counts who GIVES OUT the most reacts.

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
        self.msgs = []

     # Declare cli arguments here
    def parse_args(self):
        """Parse"""
        self.parser.description = 'Messenger Bulk Data Parsing Tool'
        self.parser.add_argument('input', help="json messenger archive file")
        self.parser.add_argument(
            '--mode', help="Specify the mode to operate in. DEFAULT: MOST_POPULAR | Options: {0}".format(modesString))
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

        # Map the messages dictionary to object
        self.msgs = self.data['messages']

    def run(self):
        if self.mode == "COUNT":
            # TODO: allow for user input bounds
            return self.countInTimeFrame(1549972846000, 1550059246000)
        elif self.mode == "MOST_POPULAR":
            return self.countMostPopularPerson()
        elif self.mode == "MOST_GIVING":
            return self.countMostGiving()
        # ...more...
        else:
            return "Please supply a mode!"

    def handleCLI(self):
        self.parse_args()
        self.setup_generic()
        return self.run()

    ## ==================== WORKERS ====================== ##
    def countInTimeFrame(self, start, end):
        count = 0
        for m in self.msgs:
            if m['timestamp_ms'] > start and m['timestamp_ms'] < end:
                count = count + 1

        return count

    # counts the total number of reacts a person has gotten in the group chat.
    # Returns a list with "most popular" person at the top.
    def countMostPopularPerson(self):
        # Gen a dictionary with participants name
        popularityDict = {}
        for person in self.participants:
            popularityDict[person] = {
                "count": 0, "thumbsDown": 0, "heartEyes": 0, "cry": 0,
                "laugh": 0, "wow": 0, "thumbsUp": 0, "angry": 0
            }

        # Go though every message, and simply count the reacts on the message.
        for m in self.msgs:
            sender = m['sender_name']

            if 'reactions' in m:
                for r in m['reactions']:
                    # Count this react regardless of its type.
                    popularityDict[sender]['count'] = popularityDict[sender]['count'] + 1
                    # Check different kinds of reacts
                    if r['reaction'] == "\u00f0\u009f\u0091\u008e":  # Thumbs Down
                        popularityDict[sender]['thumbsDown'] = popularityDict[sender]['thumbsDown'] + 1
                    if r['reaction'] == "\u00f0\u009f\u0098\u008d":  # Heart Eyes
                        popularityDict[sender]['heartEyes'] = popularityDict[sender]['heartEyes'] + 1
                    if r['reaction'] == "\u00f0\u009f\u0098\u0086":  # Laugh React
                        popularityDict[sender]['laugh'] = popularityDict[sender]['laugh'] + 1
                    if r['reaction'] == "\u00f0\u009f\u0098\u00ae":  # Wow React
                        popularityDict[sender]['wow'] = popularityDict[sender]['wow'] + 1
                    if r['reaction'] == "\u00f0\u009f\u0091\u008d":  # Thumbs up
                        popularityDict[sender]['thumbsUp'] = popularityDict[sender]['thumbsUp'] + 1
                    if r['reaction'] == "\u00f0\u009f\u0098\u00a0":  # Angry React
                        popularityDict[sender]['angry'] = popularityDict[sender]['angry'] + 1
                    if r['reaction'] == "\u00f0\u009f\u0098\u00a2":  # Cry React
                        popularityDict[sender]['cry'] = popularityDict[sender]['cry'] + 1

        return sorted(popularityDict.items(), key=lambda x: x[1]['count'], reverse=True)

        # Counts people who have GIVEN the most reacts out to other people.
        # Returns dictionary with the "most giving" at the top
        def countMostGiving(self):
            # Gen a dictionary with participants name
            givingDict = {}
            for person in self.participants:
                givingDict[person] = {
                    "count": 0, "thumbsDown": 0, "heartEyes": 0, "cry": 0,
                    "laugh": 0, "wow": 0, "thumbsUp": 0, "angry": 0
                }

               # Go though every message, and simply count the reacts on the message.
            for m in self.msgs:
                if 'reactions' in m:
                    for r in m['reactions']:
                        actor = r['actor']
                       # Count this react regardless of its type.
                        givingDict[actor]['count'] = givingDict[actor]['count'] + 1
                        # Check different kinds of reacts
                        if r['reaction'] == "\u00f0\u009f\u0091\u008e":  # Thumbs Down
                            givingDict[actor]['thumbsDown'] = givingDict[actor]['thumbsDown'] + 1
                        if r['reaction'] == "\u00f0\u009f\u0098\u008d":  # Heart Eyes
                            givingDict[actor]['heartEyes'] = givingDict[actor]['heartEyes'] + 1
                        if r['reaction'] == "\u00f0\u009f\u0098\u0086":  # Laugh React
                            givingDict[actor]['laugh'] = givingDict[actor]['laugh'] + 1
                        if r['reaction'] == "\u00f0\u009f\u0098\u00ae":  # Wow React
                            givingDict[actor]['wow'] = givingDict[actor]['wow'] + 1
                        if r['reaction'] == "\u00f0\u009f\u0091\u008d":  # Thumbs up
                            givingDict[actor]['thumbsUp'] = givingDict[actor]['thumbsUp'] + 1
                        if r['reaction'] == "\u00f0\u009f\u0098\u00a0":  # Angry React
                            givingDict[actor]['angry'] = givingDict[actor]['angry'] + 1
                        if r['reaction'] == "\u00f0\u009f\u0098\u00a2":  # Cry React
                            givingDict[actor]['cry'] = givingDict[actor]['cry'] + 1

            return sorted(givingDict.items(), key=lambda x: x[1]['count'], reverse=True)

        ## =================================================== ##


if __name__ == '__main__':
    m = MessengerParse()
    r = m.handleCLI()
    print(r)
