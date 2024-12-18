rs.initiate({
  _id: "rs0",
  version: 1,
  members: [
      { _id: 0, host: "localhost:27017" }
  ]
});

// Wait for replica set to initiate
sleep(5000);

// Create Debezium user
db = db.getSiblingDB("admin");
db.createUser({
  user: "debezium",
  pwd: "dbz",
  roles: [
      { role: "read", db: "testdb" },
      { role: "readWrite", db: "testdb" },
      { role: "clusterMonitor", db: "admin" },
      { role: "readAnyDatabase", db: "admin" }
  ]
});