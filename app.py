from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!!!'

@app.route('/my_api')
def my_api():
    return jsonify(message= 'hello this is my first api'), 200

@app.route('/not_found')
def not_found():
    return jsonify(message = 'that page not found'), 404

@app.route('/parameters')
def parameter():
    name = request.args.get('name')
    age = int(request.args.get('age'))

    if age < 18:
        return jsonify('Sorry '+ name + '. You are not allowed'), 401
    else:
        return jsonify('Welcome, ' + name), 200

@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name:str, age:int):
    if age < 18:
        return jsonify('Sorry '+name+ '. You are not allowed'),401
    else:
        return jsonify('Hello, '+ name), 200

if __name__ == '__main__':
    app.run()
