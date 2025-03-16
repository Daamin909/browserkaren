from flask import Flask, request, jsonify
from flask_cors import CORS
import messages as m

app = Flask(__name__)
CORS(app)

@app.route('/api/fetch-messages', methods=['POST'])
def fetchMessages():
    return jsonify(m.fetch_messages())

@app.route('/api/write-messages', methods=['POST'])
def writeMessages():
    data = request.get_json()['data']
    return jsonify(m.write_messages(data))

@app.route('/api/get-response', methods=['POST'])
def getResponse():
    message = request.get_json()['message']
    return jsonify( m.get_response(message))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001", debug=True)