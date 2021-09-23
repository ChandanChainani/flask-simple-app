from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import datetime
from functools import wraps

from constants import SECRET_KEY, ADMIN, CUSTOMER
from models import User, Theatre, Booking, Theatre_Bookings

def authenticate(username, password):
    user = User.table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.userid_table.get(user_id, None)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["JWT_LEEWAY"] = datetime.timedelta(weeks=7)

jwt = JWT(app, authenticate, identity)

def is_role(TYPE):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if (current_identity.role == TYPE):
                return fn(*args, **kwargs)
            return jsonify({
                'message' : 'Unauthorized access!!!'
            }), 401

        return decorator
    return wrapper

@app.route('/theatres', defaults={'name': None})
@app.route('/theatres/<name>')
def list_theatres(name):
    try:
        theatre = Theatre.get(name)
        if theatre == {}:
            return jsonify({
                "message": "Not found"
            }), 200

        return jsonify({
            "data": theatre
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Internal server error."
        }), 500


@app.route('/theatres/<name>/seats')
def left_seats(name):
    theatre = Theatre.get(name)
    if theatre == {}:
        return jsonify({
            "message": "Theatre not found"
        }), 200

    return jsonify({
        "data": {
            "seats": Theatre_Bookings.seats_left(name)
        }
    }), 200
    try:
        pass
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Internal server error."
        }), 500


@app.route('/theatre/new', methods=['POST'])
@jwt_required()
@is_role(ADMIN)
def add_theatres():
    try:
        data = request.json
        theatre_name = data.get("name", None)
        seats = data.get("seats", None)
        if theatre_name == None or seats == None:
            return jsonify({
                "message": "Missing parameter name or seats"
            }), 200

        if Theatre.exists(theatre_name):
            return jsonify({
                "message": "Theatre already exits with given name"
            }), 200

        Theatre.add(theatre_name, seats)
        return jsonify({
            "message": "Theatre added successfully"
        }), 201
    except Exception as e:
        print(e)
        return jsonify({
            "message": "Internal server error."
        }), 500


@app.route('/booking/new', methods=['POST'])
@jwt_required()
@is_role(CUSTOMER)
def add_bookings():
    data = request.json
    theatre_name = data.get("name", None)
    book_seats = data.get("seats", None)
    if theatre_name == None or book_seats == None:
        return jsonify({
            "message": "Missing parameter name or seats"
        }), 500

    if not Theatre.exists(theatre_name):
        return jsonify({
            "message": "Theatre with name not exists"
        }), 200

    if Theatre_Bookings.isBooked(theatre_name):
        return jsonify({
            "message": "Sorry no seat left"
        }), 200

    if Booking.add(current_identity.id, theatre_name, book_seats):
        return jsonify({
            "message": "Seats booked successfully"
        }), 200

    return jsonify({
        "message": "Show already booked"
    }), 200


if __name__ == '__main__':
    app.run()

