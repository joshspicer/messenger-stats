# messenger-stats

`tracy:messenger-stats josh$ python3 messengerparse.py -h`

```
usage: messengerparse.py [-h] [--mode MODE] input

Messenger Bulk Data Parsing Tool

positional arguments:
  input        json messenger archive file

optional arguments:
  -h, --help   show this help message and exit
  --mode MODE  Specify the mode to operate in. 
               DEFAULT: MOST_POPULAR
               Options: 
               
               - MOST_POPULAR: Counts how the total reacts each person
               in a group chat has received. 
               
               - COUNT: Counts how many messages
               occur in a given timeframe.

```
