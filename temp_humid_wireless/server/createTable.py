import sqlite3

def create_database():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()


def main():

    create_database()


if __name__ == "__main__":
    main()