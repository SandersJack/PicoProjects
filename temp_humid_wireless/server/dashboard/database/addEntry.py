import argparse
import sqlite3
from flask_bcrypt import Bcrypt

def create_user(username, password):
    # SQLite database connection
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    # Hash the password using bcrypt
    hashed_password = Bcrypt().generate_password_hash(password).decode('utf-8')

    # Insert the new user into the database
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new user in the SQLite database.')
    parser.add_argument('username', type=str, help='The username for the new user')
    parser.add_argument('password', type=str, help='The password for the new user')

    args = parser.parse_args()

    create_user(args.username, args.password)
    print(f"User '{args.username}' created successfully.")