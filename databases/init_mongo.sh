docker exec -it mongodb mongosh --eval "rs.initiate({_id:'rs0', members: [{_id:0, host: 'iuhkartdb.serveftp.com'}]})"
docker exec -it mongodb mongosh --eval "rs.status()"

# docker exec -it mongodb mongosh
# use demo
# db.items.insertOne({"name": "Le Van C", "age": 35})
# db.items.updateOne({"name": "Le Van C"}, {"$set": {"age": 36}})
# db.items..deleteOne({"name": "Le Van C"})