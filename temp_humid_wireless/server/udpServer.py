import socket
import sqlite3
from datetime import datetime

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

def save_data_to_database(temperature, humidity):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO sensor_data (temperature, humidity, timestamp) VALUES (?, ?, ?)',
                   (temperature, humidity, timestamp))
    conn.commit()
    conn.close()


def start_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        server_address = (SERVER_IP, SERVER_PORT)
        try:
            udp_socket.bind(server_address)
        except Exception as e:
            print(f"Error binding UDP socket: {e}")

        print(f"UDP server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            data, client_address = udp_socket.recvfrom(1024)

            key_value_pairs = data.decode('utf-8').split('&')

            # Initialize variables to store temperature and humidity
            temperature = None
            humidity = None

            # Iterate through key-value pairs to extract values
            for pair in key_value_pairs:
                key, value = pair.split('=')
                if key == 'temperature':
                    temperature = float(value)
                elif key == 'humidity':
                    humidity = float(value)

            save_data_to_database(temperature, humidity)

            print(f"Received data from {client_address}: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_udp_server()