import sys

# Receiving arguments from the command line
value1 = sys.argv[1]  # The first argument after the script name
value2 = sys.argv[2]  # The second argument after the script name


import psycopg2

# Connect to database
conn = psycopg2.connect(
    dbname="DatabaseName",
    user="User",
    password="Password",
    host= "localhost",
#    port="5432" #default 5432
)

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Insert data into a table
try:
    cur.execute("INSERT INTO table_name (first_value, second_value) \
                VALUES (%s, %s)",
                (value1, value2))
    conn.commit()  # Confirm the transaction
    print("Data entered successfully!")
except psycopg2.Error as e:
    print("Error inserting data:", e)
    conn.rollback() # Rollback the transaction in case of error

# Close the cursor and the connection
cur.close()
conn.close()