import psycopg2

# Replace these values with your database credentials
db_name = "chatroom"
db_user = "silkylounge"
db_password = "Frankfurt5!"
db_host = "localhost"

# Connect to the database
conn = psycopg2.connect(
    dbname=db_name, user=db_user, password=db_password, host=db_host
)

# Create a cursor object
cursor = conn.cursor()

# Example query: select all messages
cursor.execute("SELECT * FROM messages")

# Fetch and print the results
for row in cursor.fetchall():
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
