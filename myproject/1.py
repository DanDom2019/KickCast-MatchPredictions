from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api')
def api_info():
    return jsonify({"message": "Welcome to the mock API!"})

if __name__ == '__main__':
    app.run(debug=True)