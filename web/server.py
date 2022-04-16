# @Time    : 2022/4/14 23:32PM
# @Author  : Yasushi Oh
# @File    : server.py

"""server.py

    Borrowed from https://github.com/Eroducate/project-megabunus
    Made changes to serve as a backend template

"""

'''Dependencies:
    Flask, 
    Flask_cors, 
    json, sqlite3, 
    random, 
    random
'''

# initialize Flask app and enable CORS
from flask import Flask, request, jsonify, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_cors import CORS
import json
import sqlite3
import random
import threading
import re
app = Flask(__name__)
auth = HTTPBasicAuth()

CORS(app)

sqlite_path = "./data/"

# saves the database names
DB_NAMES = {
    "USERS": "user.db",
}

SECRET_KEY = "INSPO!"


class Cursor:
    """Cursor

    Purpose: Cursor class wraps the sqlite library
        for client to perform database operations more 
        easily.

    Fields:
        db_name: the name of the cursor to operate at first

        db_names: the range of database names the cursor 
            can choose to connect from
    """

    db_names = {}  # range of database names to choose from
    connection = None  # sqlite connection
    cursor = None  # sqlite cursor
    db_name = None  # active database's name

    def __init__(self, db_name, db_names):
        """Initializes the cursor.

        Initializes the cursor by initializing db_names and
            calling connect with db_name.

        Args:
            db_name: the database's name to connect.
            db_names: the range of database names to choose from.

        Returns:
            None

        Raises:
            None
        """
        self.db_names = db_names
        self.connect(db_name)

    def connect(self, db_name):
        """connects the cursor to another database

        connects the cursor to another database by reinitializing
            the sqlite connection and cursor

        Args:
            db_name: the database's name to initialize

        Returns:
            None

        Raises:
            Error: db name not found!
        """
        if db_name in self.db_names:
            self.connection = sqlite3.connect(
                sqlite_path + self.db_names[db_name], check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.db_name = db_name
        else:
            print("db name not found!")

    def run(self, command):
        """runs a command in the database

        runs a command in the database and
            commits it

        Args:
            command: the command to execute

        Returns:
            None

        Raises:
            Error: database execution errors, probably related with command.
        """
        lock = threading.Lock()  # threading.lock() added to prevent recursive use of cursor error
        try:
            lock.acquire(True)
            self.cursor.execute(command)
            self.connection.commit()
        finally:
            lock.release()

    def get(self, condition):
        """get one record from the database according
            to the condition

        Args:
            condition: the condition to execute

        Returns:
            the found record

        Raises:
            Error: database execution errors, probably related with command.
        """
        lock = threading.Lock()
        try:
            lock.acquire(True)
            self.cursor.execute(
                "SELECT * FROM " + self.db_name + " WHERE (" + condition + ")"
            )
        finally:
            lock.release()
            return self.cursor.fetchone()

    def getAll(self, condition=""):
        """gets all records in the database

        Args:
            condition(optional): the condition to execute,


        Returns:
            None

        Raises:
            Error: database execution errors, probably related with command.
        """

        lock = threading.Lock()
        try:
            lock.acquire(True)
            self.cursor.execute(
                "SELECT * FROM " +
                self.db_name +
                (" WHERE " if condition != "" else "") +
                condition
            )
        finally:
            lock.release()
            return self.cursor.fetchall()

    def delete(self, condition):
        """deletes the record according to the condition

        Args:
            condition: the condition to execute,


        Returns:
            None

        Raises:
            Error: database execution errors, probably related with command.
        """
        # delete the record only when it exists in the db
        self.run(
            "DELETE FROM " +
            self.db_name +
            " WHERE EXISTS (SELECT * FROM " +
            self.db_name +
            " WHERE " +
            condition +
            ") AND " +
            condition)
        return "Deleted"

    def insert(self, prop, values):
        """inserts into the record with with desired column and value

        Args:
            prop: the columns to insert(e.g: name, sex, age)

            values: the values to insert(e.g: calen, male, 19)


        Returns:
            <string>success

        Raises:
            Error: prop not found or value invalid
        """
        self.run("INSERT INTO " + self.db_name + " (" + prop + ") " +
                 "VALUES (" + values + ")")
        return "Success"

    def update(self, condition, values):
        """updates the record with with desired condition and values

        Args:
            condition: the condition to execute

            values: the values to insert(e.g: calen, male, 19)


        Returns:
            <string>success

        Raises:
            Error: value invalid or condition error or condition not found
        """
        self.run("UPDATE " + self.db_name + " SET " +
                 values + " WHERE " + condition)
        return "success"


# initialize the cursor
cursor = Cursor("USERS", DB_NAMES)


def generate_auth_token(user_id, expiration=36000):
    '''generates auth token for use

    user_id: user's id
    expiration: the time before expiration(default 600minutes)

    returns a generated token
    '''
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'user_id': user_id})


def verify_auth_token(token):
    '''verifies whether the token is valid or not

    '''
    s = Serializer(SECRET_KEY)
    # toekn valid
    try:
        data = s.loads(token)
        return data
    # token expired
    except SignatureExpired:
        return None
    # token wrong
    except BadSignature:
        return None


@auth.verify_password
def verify_password(username, password):
    '''verifies the username and password using
    basic auth.

    called when the function with decorator @auth.login_required
    is called
    '''

    #print(username, password)
    
    # verify token
    user_id = verify_auth_token(
        re.sub(r'^"|"$', '', username)
    )
    # check username and password if token invalid
    if not user_id:
        cursor.connect("USERS")
        user_id = cursor.get(
            "USERNAME = '" +
            username +
            "' AND PASSWORD = '" +
            password + "'")
        # return False if wrong password and username
        if not user_id:
            return False
        g.user_id = user_id[1]
    else:
        g.user_id = user_id.get('user_id')
    return True


def GenerateID():
    """generates a five digit random number
        """
    id = ""
    for i in range(0, 5):
        id += str(random.randint(0, 9))
    return id


@app.route('/')
def index():
    '''
    meme
    '''
    return "It Works! Yeah It's an Apache Meme"


# TODO: Make this register follow our user database structure @Sophia
@app.route('/register', methods=['POST'])
def register():
    """registers the user

        Call: /register

        Args: {"username": calen, "password": 88888888}

        Returns:
            <string>success or not

        Raises:
            Error: username and password passed in in wrong format
    """
    # the incoming username, password, and token
    incoming = json.loads(request.get_data().decode('utf-8'))

    # if token is correct, register the user in database
    cursor.connect("USERS")
    cursor.run("INSERT INTO USERS (ID,USERNAME,PASSWORD) \
    VALUES (" + GenerateID() + ",'" + incoming["username"] + "','" + incoming["password"] + "')")
    return "User Created"

# TODO: Make sure that this works after we updated register @Saksham
@app.route('/login', methods=['GET'])
@auth.login_required
def login():
    """performs user login

        performs user login by checking if the user exists,
        and returns true or false

        Call: /login

        Args: {"username": calen, "password": 88888888}

        Returns:
            <string>True if user exists, False otherwise

        Raises:
            Error: username and password passed in in wrong format
    """
    token = generate_auth_token(g.user_id)
    return jsonify({'token': str(token, encoding='utf-8')})

# TODO: Return "Notes" from the user database with the provided user id. @Saksham
@app.route('/notes', methods=['GET'])
def getNote(input_ID=None):
    """get note by id    

        Call: /notes?id=ID_OF_NOTE

        Returns:
            notes in json string
    """

    # connect to level
    cursor.connect("USER")
    return "TODO"

    # # parse parameters
    # if(input_ID):
    #     id = input_ID
    # else:
    #     id = request.args.get("id")

    # level = cursor.get("ID = " + str(id))

    # # return level or "Not Found" if level not found
    # if level != None:
    #     print('Level found!')
    #     return json.dumps(
    #         {
    #             'id': level[0],
    #             'name': level[1],
    #             'level': level[2]
    #         })
    # return "Not Found"

# TODO: Update user's info accordingly with the provided parameters. @David
@app.route('/user', methods=['POST'])
@auth.login_required
def updateUser():
    """updates user info including notes, worktime, and resttime         

        Call: /user

        Args: {"id": 00000, "name": level_a, level: {...}}

        Returns:
            <string>success

        Raises:
            Error: parameter incorrect
    """

    # # connect to levels.db
    # cursor.connect("LEVELS")

    # # parse the parameters
    # request_data = request.get_data().decode('utf-8')
    # updatedData = json.loads(request_data)
    # name = json.dumps(updatedData["localization"])
    # level = json.dumps(updatedData["clips"])
    # id = dict.get(updatedData, "id", "")

    # create or update the level according to level found in database
    # cursor.update(
    #     "ID = " + str(id),
    #     "LEVEL = '" + level + "', NAME = '" + name + "'")
    # return "success"
    return "TODO"

# Use this to initialize DB
# TODO: Change this to fit the user database structure. @Sophia
# def initUserDB():
#     UserCon = sqlite3.connect(
#                 "./data/user.db", check_same_thread=False)
#     UserCur = UserCon.cursor()
#     UserCur.execute('CREATE TABLE USERS \
#        (ID INT PRIMARY KEY     NOT NULL, \
#        USERNAME           TEXT    NOT NULL, \
#        PASSWORD           TEXT    NOT NULL); \
#        ')
#     UserCon.commit()
#     print("User DB initialized")

# initUserDB()
