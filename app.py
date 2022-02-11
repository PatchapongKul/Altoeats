from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!!!'
@app.route('/my_api')
def my_api():
    return jsonify(message= 'hello this is my first api')

if __name__ == '__main__':
    app.run()
