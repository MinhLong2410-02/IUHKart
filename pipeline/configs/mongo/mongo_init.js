// rs.initiate({
//     _id: "rs0",
//     version: 1,
//     members: [
//         { _id: 0, host: "localhost:27017" }
//     ]
// });

db = db.getSiblingDB('mydb');
db.coll.insertOne({ name: "Debezium", type: "Connector", status: "Active" })

db.createUser({
  user: "debezium",
  pwd: "dbz",
  roles: [
    { role: "read", db: "mydb" },
    { role: "readWrite", db: "mydb" },
    { role: "dbAdmin", db: "mydb" },
    { role: "clusterMonitor", db: "admin" }
  ]
});