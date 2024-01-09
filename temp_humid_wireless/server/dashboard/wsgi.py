from app import server as application

if __name__ == "__main__":
    application.run_server(debug=False, port=5050)