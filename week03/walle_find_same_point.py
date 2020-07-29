from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

## 코딩 할 준비 ##
walle=db.movies.find_one({'title':'월-E'})
walle_point=walle["point"]

movies=list(db.movies.find({'point':walle_point}))

for movie in movies:
    print(movie['title'])