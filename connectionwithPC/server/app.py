from flask import Flask, request, jsonify
#from pymongo import MongoClient

app = Flask(__name__)

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.get_json()

    # Insert data into MongoDB
    #collection.insert_one(data)
    print(data)

    return jsonify({"status": "Data received and stored in MongoDB"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)