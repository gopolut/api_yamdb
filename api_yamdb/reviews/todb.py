import sqlite3, csv


con = sqlite3.connect('c:/Users/Pavel/Documents/Ya_praktikum_python/Dev/api_yamdb/api_yamdb/db.sqlite3')
# c:\Users\Pavel\Documents\Ya_praktikum_python\Dev\api_yamdb\api_yamdb\db.sqlite3
cur = con.cursor()

with open('c:/Users/Pavel/Documents/Ya_praktikum_python/_test/genre_title.csv', encoding='utf-8') as cf:
    dict = csv.DictReader(cf)
    
    '''titles'''
    # to_db = [(i['id'], i['name'], i['year'], i['category']) for i in dict] # title
    
    '''category, genre'''
    # to_db = [(i['id'], i['name'], i['slug']) for i in dict] 
    
    '''genre_title'''
    to_db = [(i['id'], i['genre_id'], i['title_id']) for i in dict]
    
    # review
    # to_db = [(i['id'], i['text'], i['score'], i['pub_date'], i['author'], i['title_id']) for i in dict]
    
    # id,username,email,role,bio,first_name,last_name
    # to_db = [(i['id'], i['username'], i['first_name'], i['last_name'], i['email'], i['bio'], i['role']) for i in dict] # users

print(to_db)
'''titles'''
# cur.executemany('INSERT INTO reviews_title(id,name,year,category_id) VALUES (?,?,?,?)', to_db)

# reviews
# cur.executemany('INSERT INTO reviews_reviews VALUES (?,?,?,?,?,?)', to_db)

'''category, genre, genre_title'''
cur.executemany('INSERT INTO reviews_genretitle VALUES (?,?,?)', to_db)

# cur.executemany('INSERT INTO users_customuser(id,username,first_name,last_name,email,bio,role) VALUES (?,?,?,?,?,?,?)', to_db) # users
# cur.execute('DELETE FROM reviews_reviews')

con.commit()
