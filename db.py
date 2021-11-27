import sqlite3
conn = sqlite3.connect("registration_database.db")

print("Database opened successfully")

conn.execute("CREATE TABLE register (firstName TEXT, lastName TEXT, Email TEXT, username TEXT, password TEXT)")
print("Table created successfully")

conn.close()