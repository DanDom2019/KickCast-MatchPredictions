/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
// CommBank Database Seeding Script
// Make sure you're connected to your MongoDB Atlas cluster first

// Select the CommBank database
use('CommBank');

// Insert Goals (including the one you're trying to access)
db.getCollection('Goals').insertMany([
  {
    "_id": ObjectId("62a3f587102e921da1253d32"),
    "Name": "House Down Payment",
    "TargetAmount": NumberLong(100000),
    "TargetDate": new Date("2025-01-08T07:00:00.000Z"),
    "Balance": 73501.82,
    "Created": new Date("2022-06-11T07:59:50.857Z"),
    "TransactionIds": null,
    "TagIds": null,
    "UserId": ObjectId("62a29c15f4605c4c9fa7f306")
  },
  {
    "_id": ObjectId("62a3f5e0102e921da1253d33"),
    "Name": "Tesla Model Y", 
    "TargetAmount": NumberLong(60000),
    "TargetDate": new Date("2022-09-01T00:00:00.000Z"),
    "Balance": 43840.02,
    "Created": new Date("2022-06-11T08:01:20.950Z"),
    "TransactionIds": null,
    "TagIds": null,
    "UserId": ObjectId("62a29c15f4605c4c9fa7f306")
  },
  {
    "_id": ObjectId("62a3f62e102e921da1253d34"),
    "Name": "Trip to London",
    "TargetAmount": NumberLong(3500),
    "TargetDate": new Date("2022-08-02T00:00:00.000Z"),
    "Balance": 753.89,
    "Created": new Date("2022-06-11T08:02:38.236Z"),
    "TransactionIds": null,
    "TagIds": null,
    "UserId": ObjectId("62a29c15f4605c4c9fa7f306")
  }
]);

// Insert a User
db.getCollection('Users').insertOne({
  "_id": ObjectId("62a29c15f4605c4c9fa7f306"),
  "Name": "Danny",
  "Email": "danny@example.com", 
  "Password": "$2a$11$hashedPasswordExample",
  "AccountIds": [],
  "GoalIds": [],
  "TransactionIds": []
});

// Check what was inserted
console.log("Goals inserted:", db.getCollection('Goals').countDocuments());
console.log("Users inserted:", db.getCollection('Users').countDocuments());
