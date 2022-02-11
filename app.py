from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'altoeats.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('DB created')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB dropped')

@app.cli.command('db_seed')
def db_seed():
    padthai = Food(food_name = 'Pad Thai',
                   food_type = 'noodle',
                   price = 100,
                   cuisine = 'Thai')

    spaghetti = Food(food_name='Sphagetti',
                  food_type='noodle',
                  price=200,
                  cuisine = 'Italian')

    db.session.add(padthai)
    db.session.add(spaghetti)

    test_user = User(first_name = 'Patchapong',
                     last_name = 'Kulthumrongkul',
                     email = 'patchapong.kul@gmail.com',
                     password = 'asdf')

    db.session.add(test_user)
    db.session.commit()
    print("Database seeded")



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

@app.route('/foods', methods = ['GET'])
def foods():
    food_list = Food.query.all()
    result = foods_schema.dump(food_list)
    return jsonify(result)

@app.route('/users', methods = ['GET'])
def users():
    user_list = User.query.all()
    result = users_schema.dump(user_list)
    return jsonify(result)

# Create Database
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique= True)
    password = Column(String)

class Food(db.Model):
    __tablename__ = 'foods'
    food_id = Column(Integer, primary_key= True)
    food_name = Column(String)
    food_type = Column(String)
    price = Column(Float)
    cuisine = Column(String)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email')

class FoodSchema(ma.Schema):
    class Meta:
        fields = ('food_id', 'food_name', 'food_type', 'price', 'cuisine')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

food_schema = FoodSchema()
foods_schema = FoodSchema(many = True)

if __name__ == '__main__':
    app.run()
