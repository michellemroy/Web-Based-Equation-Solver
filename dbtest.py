import sqlite3

conn = sqlite3.connect('equation.db')
print("Opened database successfully")

# conn.execute('DROP TABLE LOGIN;')
# conn.execute('CREATE TABLE LOGIN(Email TEXT, Password TEXT);')
# print("Table created successfully");

# email = 'michelle'

# conn.execute('INSERT INTO LOGIN VALUES ("michelle","171");')
# conn.commit()
# res = conn.execute("SELECT * FROM LOGIN WHERE email='michelle';")
# for row in res:
#     print(row)
# print("Table created successfully");

#conn.execute('CREATE TABLE HISTORY(Email TEXT, eq1 TEXT, eq2 TEXT);')

res = conn.execute("SELECT * FROM HISTORY")
for row in res:
    print(row)
conn.close()