import pymongo 

conn = pymongo.MongoClient()
db = conn['info']

post = {
    'id': 1,
    'test': 'test123'
}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
db.list_collection_names()