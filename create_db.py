import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS hotels (hotel_id text PRIMARY KEY, name text, rank real, daily real, city text)"

create_hotel = "INSERT INTO hotels VALUES ('alpha', 'Alpha Hotel', 4.3, 345.30, 'Rio de Janeiro')"

cursor.execute(create_table)
cursor.execute(create_hotel)

connection.commit()
connection.close()