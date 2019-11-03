# PS_backend_task_Oct_2019
************************
## backend.py, creatingdb.py    -   README
************************

creatingdb.py fills example data source with data from OMDb API.
Given data source contains only titles of movies.
The program backend.py is using command line interface and is capable of:

1. Sorting Movies by column names
2.Filtering by:
  - Name of column
  - Movies that was nominated  for Oscar but did not win any.
  - Movies that won more than 80% of nominations
  - Movies that earned more than 100,000,000 $
3. Comparing movies by columns names
4. Adding movies to data source
5. Showing current highscores in :
   - Runtime
   - Box office earnings
   - Most awards won
   - Most nominations
   - Most Oscars
   - Highest IMDB Rating
6. Checking titles in DB

Requirements
-------------

- Python 3.7 +
- requests
- pytest
- sqlite3
- argparse


Initializing backend.py
------------------------

To properly use backend.py download Backend_movies.sqlite and save it as 'Backend_movies - Copy.sqlite'.
Download: creatingdb.py, backend.py and backend_test.py.

In creatingdb.py please enter your own API key (LINE 17: 'apikey': 'ENTER_YOUR_KEY_HERE'). 
You need to generate your own API key here http://www.omdbapi.com/apikey.aspx.
Please do the same for backend.py (LINE 182: 'apikey': 'ENTER_YOUR_KEY_HERE') and backend_test.py (LINE 181: 'apikey': 'ENTER_YOUR_KEY_HERE') using the same key.

(Please navigate to folder containing the file in your command line first)
Initialize database for backend.py by executing creatingdb.py - by writing python creatingdb.py in shell.


Usage of backend.py
--------------------
To use backend.py just write python backend.py with argument corresponding to desirable functionality.

List of arguments is represented below:

  -h, --help            show this help message and exit  
  -columns              prints names of columns. e.g. -columns  
  -s [SORT [SORT ...]]  sorts by one or two columns. e.g. -s year title  
  -f [FILTER [FILTER ...]]
                        filters. possibilities: column names + "oscar",
                        "nominations" and "earnings". e.g. -f cast Anne / -f oscar / -f nominations                        
  -c [COMPARE [COMPARE ...]]
                        compares two movies by the column. e.g. -c runtime
                        Gods Memento                        
  -hi                   prints current highscore. e.g. -hi  
  -add ADD              adds movie to a sqlite db. e.g. -add movie_title  
  -check CHECK          check record in sqlite db. e.g. -check Memento

In case of title consisting two or more words please use ' ' signs 


Columns to sort/filter/compare by:

'id', 'title', 'year', 'runtime', 'genre', 'director', 'cast', 'writer', 'language', 'country', 'awards', 'imdb_rating', 'imdb_votes', 'box_office'


List of additional filtering arguments:

- oscar - Movies that were nominated for Oscar but did not win any,
- nominations - Movies that won more than 80% of nominations,
- earnings - Movies that earned more than 100,000,000 $.

Testing backend.py (backend_test.py)
--------------------

There is a possibility of running unit tests performed by writing 'python -m pytest' in the shell. (Please navigate to folder containing the file in your command line)
