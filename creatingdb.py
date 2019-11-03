import sqlite3
import requests

conn = sqlite3.connect('Backend_movies.sqlite')
query = conn.execute("SELECT * From MOVIES")
cols = [column[0] for column in query.description]
db = query.fetchall()
conn.close()

titles = [row[1] for row in db] 

# extracting data from API
def populating_the_table(title):
    link = "http://www.omdbapi.com"
    parameters = {
        't': title,
        'apikey': 'ENTER_YOUR_KEY_HERE'
    }
    response = requests.get(link,params=parameters)

    return [(x, response.json()[x]) for x in response.json().keys()]

def data_entry():
    for title in titles:
        down_api = populating_the_table(title.strip())
        item = (down_api[1][1],down_api[4][1],down_api[5][1],down_api[6][1],down_api[8][1],down_api[7][1],
                down_api[10][1],down_api[11][1],down_api[12][1],down_api[16][1],down_api[17][1],down_api[21][1],
                title)
        sql = ''' UPDATE MOVIES SET YEAR=?,RUNTIME=?,GENRE=?,DIRECTOR=?,CAST=?,WRITER=?,LANGUAGE=?,COUNTRY=?,
                AWARDS=?,IMDb_Rating=?,IMDb_votes=?,BOX_OFFICE=? WHERE TITLE=?'''
        c.execute(sql, item)
        conn.commit()

conn = sqlite3.connect('Backend_movies - Copy.sqlite')
c = conn.cursor()
data_entry()
conn.close()