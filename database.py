import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="data_dapodik"
)

mycursor = mydb.cursor()