import mysql.connector

conn = mysql.connector.connect(
    host="crossover.proxy.rlwy.net",
    user="root",
    password="HvggmzTMICIevEUhcwOtTgTfkkNymPNA",
    database="railway",
    port=14333
)
cursor = conn.cursor()

print("Connecting to live Railway Database...")

# Read your schema file
with open('database_schema.sql', 'r') as file:
    sql_script = file.read()

sql_commands = sql_script.split(';')

# Execute each command on the live server
for command in sql_commands:
    if command.strip():
        cursor.execute(command)

conn.commit()
print("Success! Live Database Tables Created.")
cursor.close()
conn.close()