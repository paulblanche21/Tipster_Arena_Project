import psycopg2

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        user="silkylounge",
        password="Frankfurt5!",
        database="postgres"
    )

    # Enable autocommit to create a new database
    conn.autocommit = True

    # Create a cursor object
    cursor = conn.cursor()

    # Create a new database
    cursor.execute("CREATE DATABASE chatroom")

    # Disable autocommit
    conn.autocommit = False
    # Fetch the result of the query
    result = cursor.fetchone()
    # Check if the result is not None
    if result is not None:
        print("The database exists")
    else:
        print("The database does not exist")

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print("Database created successfully")

except Exception as e:
    print("An error occurred:", e)
