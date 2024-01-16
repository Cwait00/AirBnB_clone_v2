# create_state.py

import MySQLdb

def create_state(state_name):
    # Connect to the MySQL database
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="thenjiwe24", db="hbnb_dev_db", auth_plugin='mysql_native_password')

    # Create a cursor object to interact with the database
    cursor = db.cursor()

    # Execute an SQL query to insert a new state
    query = f"INSERT INTO states (name) VALUES ('{state_name}')"

    try:
        # Execute the query
        cursor.execute(query)

        # Commit the changes to the database
        db.commit()

        print(f"State '{state_name}' created successfully.")
    except Exception as e:
        # Rollback in case of an error
        db.rollback()
        print(f"Error: {e}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

if __name__ == "__main__":
    # Run the script with a specific state name (e.g., California)
    create_state("California")
