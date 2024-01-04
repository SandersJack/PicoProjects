import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

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
            print(f"Received data from {client_address}: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_udp_server()