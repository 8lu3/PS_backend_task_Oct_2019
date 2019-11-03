import sqlite3
import requests

class BackendTask(object):
    
    def __init__(self):     
        self.db=self.download_db()
        self.new_db=self.data_processing()

    def download_db(self):
        conn = sqlite3.connect('Backend_movies - Copy.sqlite')
        c = conn.cursor()
        query = c.execute("SELECT * FROM MOVIES")
        cols = [column[0] for column in query.description]
        db = c.fetchall()
        conn.close()
        self.column_names=[col.lower() for col in cols]
        self.name_dict=dict(zip(self.column_names,range(len(self.column_names))))
        return db

    # missing values, changing types, adding columns for further analysis
    def data_processing(self):
        new_db=[]
        for idx,row in enumerate(self.db):
            new_row=[]
            for idy,place in enumerate(row):
                if place=='N/A' or place=='True':
                    if idy==13 or idy==2 or idy==12:
                        new_row+=[0]
                    else:
                        new_row+=['0']
                elif idy==2 and type(place)==str:
                    new_row+=[int(place.split('–')[0])]
                elif idy==3:
                    h=str(int(place.split()[0])//60)
                    if int(place.split()[0])%60<10:
                        m=str('0'+str(int(place.split()[0])%60))
                    else:
                        m=str(int(place.split()[0])%60)
                    new_row+=[h+'h'+m+'m']
                elif idy==12 and type(place)==str:
                    new_row+=[int(place.replace(',',''))]
                elif idy==13:
                    new_row+=[int(place.split('$')[1].replace(',',''))]
                else:
                    new_row+=[place]
            nom_win_list=[place for place in row[10].split(' ') if place.isdigit()]
            (awards,nominations,oscars) =self.check_highscores_awards(nom_win_list,row[10])
            new_row+=[awards,nominations,oscars]
            new_db+=[(new_row)]
        return new_db

    # how many oscars, nominations and wins there were
    def check_highscores_awards(self,digits_list,awards_col):
        ans=[]
        nom_win_list = [int(i) for i in digits_list]
        if len(nom_win_list)==3:
                if 'Nominated for' in awards_col:
                        ans=[nom_win_list[1],nom_win_list[0]+nom_win_list[2],0]
                elif 'Won' in awards_col:
                        ans=[nom_win_list[0]+nom_win_list[1],nom_win_list[2],nom_win_list[0]]
        elif len(nom_win_list)==2:
            ans=[nom_win_list[0],nom_win_list[1],0]
        elif len(nom_win_list)==1:
            if 'wins' in awards_col:
                ans=[nom_win_list[0],0,0]
            else:
                ans=[0,nom_win_list[0],0]
        else:
            ans=[0,0,0]
        return ans

    def check_record(self,check,my_db=None):
        if my_db==None:
            my_db=self.db
        place = [(index1,index2) for index1,value1 in enumerate(my_db) for index2,value2 in enumerate(value1) if value2==check]
        if place != []:
            index_place = place[0][0]
            ans = my_db[index_place]
        else:
            ans = []
        return ans

    def sorting_by_multiple_columns(self,fir,sec='id',my_db=None,rev=False):
        if type(fir)==str:
            first=self.name_dict[fir]
        else:
            first=fir
        if type(sec)==str:
            second=self.name_dict[sec]
        else:
            second=sec
        if my_db==None:
            my_db=self.new_db
        elif my_db=='1':
            my_db=self.db
        sorted_db=[]
        # try:
        for x in sorted(my_db,key=lambda x:(x[first],x[second]), reverse=rev):
            if self.check_for_zeros(x[first],x[second],rev):
                pass
            else:
                sorted_db+=[x]
        # except:
        #     print("Can't sort by two types of columns, sorting by the first")
        #     for x in sorted(my_db,key=lambda x:x[first], reverse=rev):
        #         if self.check_for_zeros(x[first],0,rev):
        #             pass
        #         else:
        #             sorted_db+=[x]
        return sorted_db

    def check_for_zeros(self,first,second,rev=False):
        if rev==False and (first=='0' or second=='0'):
            return 1
        else:
            return 0

    # for movies that won more than 80% of nominations filter
    def check_awards(self,digits_list,awards_col):
        ans=0
        nom_win_list = [int(i) for i in digits_list]
        sum_nom_win=sum(nom_win_list)
        if len(nom_win_list)==3:
                if 'Nominated for' in awards_col:
                        ans=nom_win_list[1]/sum_nom_win
                elif 'Won' in awards_col:
                        ans=(nom_win_list[0]+nom_win_list[1])/sum_nom_win
        elif len(nom_win_list)==2:
            ans=nom_win_list[0]/sum_nom_win
        elif len(nom_win_list)==1:
            if 'wins' in awards_col:
                ans=nom_win_list[0]/sum_nom_win
            else:
                ans=0
        else:
            ans=0
        return ans

    def filter_task(self,which_column, filtr=None,db=None):
        filtered = []
        if db==None:
            db=self.db
        if which_column in self.name_dict.keys():
            which=self.name_dict[which_column]
            filtered = [[row[1],row[which]] for row in db for place in str(row[which]).split(',') if filtr.lower() in place.lower()]
        else:
            filter_dict={'oscar':3,'nominations':4,'earnings':5}
            which=filter_dict[which_column]
            if which==3: # nominated for oscars buy didn't win any
                filtered = [[row[1],row[10]] for row in db for place in row[10].split(',') if 'Nominated for' in place and 'Oscar' in place]
            elif which==4: # won more than 80% of nominations
                for row in db:
                    nom_win_list=[place for place in row[10].split(' ') if place.isdigit()]
                    awards_perc=self.check_awards(nom_win_list,row[10])
                    if awards_perc>=0.7:
                        filtered+=[[row[1],row[10]]]
            elif which==5: # box office more than 100 000 000
                pomoc =['N/A','','True']
                for row in db:
                    for place in row[13].split('$'):
                        if place not in pomoc and int(place.replace(',',''))>100000000:
                                filtered+=[[row[1],row[-1]]]
        return filtered
        #comparing based on column names
    def compare_task(self,which_column, title_one=None,title_two=None):
        row_one = self.check_record(title_one,my_db=self.new_db)
        row_two = self.check_record(title_two,my_db=self.new_db)
        which=self.name_dict[which_column]
        if row_one!=[] and row_two!=[]:
            ans=([row_one[1], row_one[which]], [row_two[1], row_two[which]])
        else:
            ans='No title in directory'
        return ans

    # extracting data from API
    def populating_the_table(self,title):
        link = "http://www.omdbapi.com"
        parameters = {
            't': title,
            'apikey': 'ENTER_YOUR_KEY_HERE'
        }
        response = requests.get(link,params=parameters)
        if response.json()['Response']=='False':
            return 'NO'
        return [(x, response.json()[x]) for x in response.json().keys()]
    # check if exist in api, check if in db, if not add
    def adding_movies(self,title):
        movie_from_db = self.populating_the_table(title)
        if movie_from_db=='NO':
            print('No such movie in omdbapi')
        else:
            conn = sqlite3.connect('Backend_movies - Copy.sqlite')
            c = conn.cursor()
            c.execute('SELECT * FROM MOVIES WHERE TITLE=?',[title])
            entry = c.fetchone()
            if entry is None:
                item = (movie_from_db[1][1],movie_from_db[4][1],movie_from_db[5][1],movie_from_db[6][1],movie_from_db[8][1],
                        movie_from_db[7][1],movie_from_db[10][1],movie_from_db[11][1],movie_from_db[12][1],movie_from_db[16][1],
                        movie_from_db[17][1],movie_from_db[21][1],title)
                sql = ''' INSERT INTO MOVIES(YEAR,RUNTIME,GENRE,DIRECTOR,CAST,WRITER,LANGUAGE,COUNTRY,
                        AWARDS,IMDb_Rating,IMDb_votes,BOX_OFFICE,TITLE) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''
                c.execute(sql, item)
                conn.commit()
                print('New entry added')
            else:
                print('Already in db')
            conn.close()
            self.db=self.download_db()
            self.new_db=self.data_processing()
        return('Done')
    # best scores in chosen categories
    def highscores(self):
        run = self.sorting_by_multiple_columns(3,my_db=self.new_db,rev=True)[0]
        box = self.sorting_by_multiple_columns(13,my_db=self.new_db,rev=True)[0]
        won = self.sorting_by_multiple_columns(14,my_db=self.new_db,rev=True)[0]
        nominations = self.sorting_by_multiple_columns(15,my_db=self.new_db,rev=True)[0]
        oscars = self.sorting_by_multiple_columns(16,my_db=self.new_db,rev=True)[0]
        rating = self.sorting_by_multiple_columns(11,my_db=self.new_db,rev=True)[0]
        return [['Runtime',run[1],run[3]],['Box office earnings',box[1],'$'+str(box[13])],
                ['Most awards won',won[1],won[14]],['Most nominations',nominations[1],nominations[15]],
                ['Most Oscars',oscars[1],oscars[16]],['Highest IMDB Rating',rating[1],rating[11]]]

    #functions for printing answers
    def printing_with_cols(self,columns,my_db=None):
        print_df=[]
        if my_db==None:
            my_db=self.new_db
        which=[self.name_dict[col] for col in columns]
        if len(columns)==1 and columns!=['title']:
            print_df=[('title',*columns)]
            print_df+=[(row[1],row[which[0]]) for row in my_db]
        elif len(columns)==1:
            print_df=[('title')]
            print_df+=[row[1] for row in my_db]
        else:
            print_df=[(row[1],row[which[0]],row[which[1]]) for row in my_db]
        for row in print_df:
            print(row)

    def plain_printing(self,col,my_ans):
        print(col)
        if my_ans=='No title in directory':
            print(my_ans)
        else:
            for row in my_ans:
                print(row)


class TestBackendTask(object):
    
    def setup(self):
        self.tbt = BackendTask()
    
    def test_column_names(self):
        x = ['id', 'title', 'year', 'runtime', 'genre', 'director', 'cast', 'writer', 'language', 'country', 'awards', 'imdb_rating', 'imdb_votes', 'box_office']
        assert x == self.tbt.column_names

    def test_s_cast_director(self):
        x = [29, 'The Pianist', 2002, '2h30m', 'Biography, Drama, Music, War', 'Roman Polanski', 'Adrien Brody, Emilia Fox, Michal Zebrowski, Ed Stoppard', 'Ronald Harwood (screenplay), Wladyslaw Szpilman (book)', 'English, German, Russian', 'UK, France, Poland, Germany', 'Won 3 Oscars. Another 52 wins & 73 nominations.', 8.5, 659004, 32519322, 55, 73, 3]
        assert x == self.tbt.sorting_by_multiple_columns('cast','director')[0]

    def test_s_year_rev(self):
    	x = [11, 'Joker', 2019, '2h02m', 'Crime, Drama, Thriller', 'Todd Phillips', 'Joaquin Phoenix, Robert De Niro, Zazie Beetz, Frances Conroy', 'Todd Phillips, Scott Silver, Bob Kane (based on characters created by), Bill Finger (based on characters created by), Jerry Robinson (based on characters created by)', 'English', 'USA, Canada', '0', 8.9, 360218, 0, 0, 0, 0]
    	assert x == self.tbt.sorting_by_multiple_columns('year','imdb_votes',rev=True)[0]

    def test_compare_one(self):
    	x = (['Memento', '1h53m'],['Shazam', '0h06m'])
    	assert x == self.tbt.compare_task('runtime','Memento','Shazam')

    def test_compare_two(self):
    	x = (['The Shawshank Redemption', 'English'],['Gods', 'Polish'])
    	assert x == self.tbt.compare_task('language','The Shawshank Redemption','Gods')

    def test_f_cast(self):
    	x = ['Cinema Paradiso', 'Antonella Attili, Enzo Cannavale, Isa Danieli, Leo Gullotta']
    	assert x == self.tbt.filter_task('cast','Anna')[0]

    def test_f_language(self):
    	x = [['The Hunt', 'Danish, English, Polish']]
    	assert x == self.tbt.filter_task('language','Dan')

    def test_highscore(self):
    	x = ['Runtime', 'Gone with the Wind', '3h58m']
    	assert x == self.tbt.highscores()[0]
   
    def test_add(self):
    	x = 'Done'
    	assert x == self.tbt.adding_movies('Shazam')