from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

## 코딩 할 준비 ##
walle=db.movies.find_one({'title':'월-E'})
print(walle['point'])