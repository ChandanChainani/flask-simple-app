from random import randint
from constants import ADMIN, CUSTOMER


class User(object):
    users = []
    table = {}
    userid_table = {}

    def __init__(self, id, username, password, role = CUSTOMER):
        self.id = id
        self.username = username
        self.password = password
        self.role     = role

    def __str__(self):
        return "User(id='%s')" % self.id

    @classmethod
    def seed(cls):
        cls.users = [
            cls(1,  'user1', 'u1',  ADMIN)
        ] + [cls(_id, f"user{_id}", "u{}".format(_id)) for _id in range(2, 11)]

        cls.table = {u.username: u for u in cls.users}
        cls.userid_table = {u.id: u for u in cls.users}


class Theatre(object):
    theatres = []
    table = {}

    @classmethod
    def add(cls, theatre_name, seats):
        theatre = {
           "name": theatre_name,
           "seats": seats,
        }
        cls.theatres.append(theatre)
        cls.table[theatre_name] = theatre
        cls.table[theatre_name]["id"] = len(cls.theatres) - 1

    @classmethod
    def get(cls, name = None):
        if name == None:
            return cls.theatres
        theatre = cls.table.get(name, None)
        if theatre == None:
            return {}
        print(theatre)
        return theatre

    @classmethod
    def exists(cls, name):
        return cls.table.__contains__(name)

    @classmethod
    def seed(cls):
        theatres = [
            "Victory Theatre",
            "City Pride",
            "City Pride Royal Cinemas",
            "Vasant Theatre",
            "Neelayam Theatre",
            "PVR Cinemas",
        ]

        cls.theatres = [{
            "name": theatre_name,
            "seats": randint(25, 50)
        } for theatre_name in theatres]

        cls.table = {theatre["name"]: { "name": theatre["name"], "seats": theatre["seats"], "id": index } for index, theatre in enumerate(cls.theatres)}


class Booking(object):
    table = {}

    @classmethod
    def add(cls, user_id, theatre_name, book_seats):
        if cls.table.get(theatre_name, None) == None:
            cls.table[theatre_name] = {
                "seats": 0,
                "users": {}
            }

        if cls.table[theatre_name]["users"].__contains__(user_id):
            return False

        cls.table[theatre_name]["seats"] += book_seats
        cls.table[theatre_name]["users"][user_id] = True
        return True

    @classmethod
    def exists(cls, name):
        return cls.table.__contains__(name)


class Theatre_Bookings(object):
    @classmethod
    def isBooked(cls, name):
        return Theatre.exists(name) and Booking.exists(name) and (Theatre.get(name)["seats"] - Booking.table[name]["seats"]) == 0


User.seed()
Theatre.seed()

