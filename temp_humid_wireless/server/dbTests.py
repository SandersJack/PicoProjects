import sqlite3

def print_all_data():
    conn = sqlite3.connect('data/sensor_data.db')
    cursor = conn.cursor()

    # Select all rows from the sensor_data table
    cursor.execute('SELECT * FROM sensor_data')
    rows = cursor.fetchall()

    # Print the header
    print("ID\tTemperature\tHumidity\tTimestamp")

    # Iterate through the rows and print each record
    for row in rows:
        print("\t".join(map(str, row)))

    conn.close()

def main():

    print_all_data()


if __name__ == "__main__":
    main()