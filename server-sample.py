# @Time    : 2021/6/24 12:38 AM
# @Author  : Yasushi Oh
# @File    : server.py

"""server.py

    This file provides backend server functionality 
    for Self-Reliance Portal. It mainly handles user 
    login, regstration, and other operations involving 
    the database. It also handles some OSS related stuff.

"""

'''Dependencies:
    Flask, 
    Flask_cors, 
    json, sqlite3, 
    random, 
    oss, 
    random
'''

# initialize Flask app and enable CORS
import base64
import oss2
from flask import Flask, request, jsonify, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_cors import CORS
import json
import sqlite3
import random
from functools import reduce
import threading
import re
app = Flask(__name__)
auth = HTTPBasicAuth()

CORS(app)

sqlite_path = "/ero_sqlite/data/"

# saves the database names
DB_NAMES = {
    "SETTINGS": "settings.db",
    "USERS": "users.db",
    "LEVELS": "levels.db",
    "ACHIEVEMENTS": "achievements.db",
    "STATS": "stats.db",
}

# registration code, TODO:should be deleted in the future.
RegistrationCode = "Eroducate!"
SECRET_KEY = "Eroducate!"


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
cursor = Cursor("LEVELS", DB_NAMES)


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
@auth.login_required
def index():
    '''
    meme
    '''
    return "It Works! Yeah It's an Apache Meme"


@app.route('/register', methods=['POST'])
def register():
    """registers the user

        Call: /register

        Args: {"token" 123456, "username": calen, "password": 88888888}

        Returns:
            <string>success or not

        Raises:
            Error: username and password passed in in wrong format
    """
    # the incoming username, password, and token
    incoming = json.loads(request.get_data().decode('utf-8'))

    # if token is correct, register the user in database
    if incoming["token"] == RegistrationCode:
        cursor.connect("USERS")
        cursor.run("INSERT INTO USERS (ID,USERNAME,PASSWORD) \
      VALUES (" + GenerateID() + ",'" + incoming["username"] + "','" + incoming["password"] + "')")
        return "User Created"

    return "Invalid Token!"


def initStatDB(id):
    """init Stat database by level id
    """
    cursor.connect("STATS")
    if id == "" or cursor.get("ID = " + str(id)) == None:
        stat_init = json.dumps(0)
        playtime_init = json.dumps([])
        choice_table_init = []

        level = json.loads(getLevel(id))
        clip_num = len(json.loads(level['level']))

        # table size based on choices_num for each clip
        for row in range(clip_num):
            choice_num = len(json.loads(level['level'])[row]['choices'])
            choice_table_init += [[0]*choice_num]
        cursor.connect("STATS")
        cursor.insert("ID, PLAYER_COUNT, PLAY_TIME,CHOICE_TABLE", id + ",'" +
                      stat_init + "','" + playtime_init + "','" + json.dumps(choice_table_init) + "'")
        return "Stats Level Initialized!"


@app.route('/stat/add_player', methods=['POST'])
@auth.login_required
def increasePlayerCount():
    """Increase the level's player count by 1 

        Call: /stat/add_player?id=ID_OF_LEVEL

        Returns:
            <string>success or not

        Raises:
            Error: statDb not found
    """
    cursor.connect("STATS")
    id = request.args.get("id")
    initStatDB(id)
    player_count = cursor.get("ID = " + str(id))[1]+1

    cursor.update(
        "ID = " + str(id),
        "PLAYER_COUNT='" + str(player_count) + "'"
    )
    return "Success!"


@app.route('/stat/count_choice', methods=['POST'])
def countPlayerChoice():
    """Increase the option's chose count by 1 

        Call: /stat/count_choice?id=ID_OF_LEVEL&clipIndex=INDEX_OF_CLIP&choiceIndex=INDEX_OF_CHOICE

        Returns:
            <string>success or not

        Raises:
            Error: INDEX not found
    """
    cursor.connect("STATS")
    id = request.args.get("id")
    clip_index = int(request.args.get("clipIndex"))
    choice_index = int(request.args.get("choiceIndex"))
    initStatDB(id)

    level = json.loads(getLevel(id))
    cursor.connect("STATS")
    clip_num = len(json.loads(level['level']))

    choice_table = json.loads(cursor.get("ID = " + str(id))[3])

    # choice_num=len(json.loads(level['level'])[0]['choices'])
    updated_choice_table = []

    # table size based on choices_num for each clip
    for row in range(clip_num):
        updated_choice_table.append([])

        choice_num = len(json.loads(level['level'])[row]['choices'])

        if row < len(choice_table):
            for col in range(choice_num):
                if col < len(choice_table[row]):
                    updated_choice_table[row] += [choice_table[row][col]]
                else:
                    updated_choice_table[row] += [0]
        else:
            updated_choice_table[row] += [0]*choice_num

    updated_choice_table[clip_index][choice_index] += 1

    cursor.update(
        "ID = " + str(id),
        "CHOICE_TABLE='" + json.dumps(updated_choice_table) + "'"
    )
    return "Success!"


@app.route('/stat/submit_choice', methods=['GET'])
def submitChoice():
    """get the percentage of the choice 

        Call: /stat/submit_choice?id=ID_OF_LEVEL&clipIndex=INDEX_OF_CLIP&choiceIndex=INDEX_OF_CHOICE

        Returns:
            <string>percentage n (0 < n < 1)

        Raises:
            Error: Missing Data
    """
    cursor.connect("STATS")
    id = request.args.get("id")
    clip_index = int(request.args.get("clipIndex"))
    choice_index = int(request.args.get("choiceIndex"))
    choice_table = json.loads(cursor.get("ID = " + str(id))[3])
    total_player = sum(choice_table[clip_index])
    chosen_player = choice_table[clip_index][choice_index]
    return "Oops! No one has played this clip :(" if total_player == 0 else str(round(float(chosen_player/total_player), 2))


@app.route('/stat/submit_time', methods=['POST'])
def submitPlayTime():
    """submit the level's playtime of the player 

        Call: /stat/submit_time?id=id=ID_OF_LEVEL&time=PLAYTIME_OF_LEVEL

        Returns:
            <string>success or not

        Raises:
            Error: Level ID Not Found
    """
    cursor.connect("STATS")
    id = request.args.get("id")
    time = request.args.get("time")

    if id == "" or cursor.get("ID = " + str(id)) == None:
        return "ERROR: Level ID Not Found, Init with initStatDB."
    else:
        playTime_list = json.loads(cursor.get("ID = " + str(id))[2])
        playTime_list.append(float(time))
        cursor.update(
            "ID = " + str(id),
            "PLAY_TIME='" + json.dumps(playTime_list) + "'"
        )
        return "Success!"

@app.route('/stat/CT', methods=['GET'])
def getChoiceTable():
    """get the 2d Array of the choice distributions

        Call: /stat/CT?id=id=ID_OF_LEVEL

        Returns:
            <string>2d Array of the choice distributions

        Raises:
            Error: Level ID Not Found
    """

    cursor.connect("STATS")
    id = request.args.get("id")
    choice_table = json.loads(cursor.get("ID = " + str(id))[3])
    return json.dumps(choice_table)

@app.route('/stat', methods=['GET'])
def getStat():
    """get all stat by id    

        Call: /stat?id=ID_OF_LEVEL

        Returns:
            stat in json string
    """
    cursor.connect("STATS")


    stat = cursor.getAll()

    output = []
    for i in range(0, len(stat)):
        output.append({
            'id': stat[i][0],
            'playerCount': stat[i][1],
            'playTime': stat[i][2]
        })
    return json.dumps(output)

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


@app.route('/settings', methods=['POST'])
@auth.login_required
def composeSetting():
    """creates or updates a setting           

        Call: /settings

        Args: {"id": 00000, "name": setting_a, localization: {...}}

        Returns:
            <string>success

        Raises:
            Error: parameter incorrect
    """
    # connect to settings.db
    cursor.connect("SETTINGS")

    # decodes the data and loads them into id, name, and setting
    request_data = request.get_data().decode('utf-8')
    updatedData = json.loads(request_data)
    id = updatedData["id"]
    name = updatedData["name"]
    setting = json.dumps(updatedData["localization"])

    # decide to create or update the setting if setting already exists in db
    if id == "" or cursor.get("ID = " + str(id)) == None:
        cursor.insert("ID, NAME, PROP", GenerateID() +
                      ",'" + name + "','" + setting + "'")
        print("Created Setting")
        return "success"
    else:
        cursor.update(
            "ID = " + str(id),
            "PROP = '" + setting + "', NAME = '" + name + "'")
        return "success"


@app.route('/settings', methods=['GET'])
def getSettings():
    """get all settings       

        Returns:
            settings in json string
    """
    # connect to settings.db
    cursor.connect("SETTINGS")

    # get settings in list
    settings = cursor.getAll()

    # format the settings and returns it in json string
    outputList = []
    for i in range(0, len(settings)):
        outputList.append({
            'id': settings[i][0],
            'name': settings[i][1],
            'localization': settings[i][2]
        })
    return json.dumps(outputList)


@app.route('/setting', methods=['GET'])
def getSettingByName():
    """get a setting by name    

        Call: /setting?name=NAME_OF_SETTING

        Returns:
            <string>success

        Raises:
            Error: parameter incorrect
    """

    # connects to database
    cursor.connect("SETTINGS")

    # get the name and finds it
    name = request.args.get("name")
    setting = cursor.get("NAME = '" + str(name) + "'")

    # returns the setting if found, else return "Not Found"
    if setting != None:
        print('found!')
        return setting[2]
    return "Not Found"


@app.route('/settings', methods=['DELETE'])
@auth.login_required
def deleteSetting():
    """deletes a setting by id

        Call: /setting?id=ID_OF_SETTING

        Returns:
            <string>deleted

        Raises:
            Error: parameter incorrect
    """
    # get the id and deletes the setting, return "Empty Data" if settings not found
    id = request.args.get("id")
    if(id == ""):
        return "Empty Data"
    cursor.connect("SETTINGS")
    cursor.delete("ID = " + str(id))
    return "deleted"


@app.route('/level', methods=['POST'])
@auth.login_required
def composeLevel():
    """creates or updates a level         

        Call: /level

        Args: {"id": 00000, "name": level_a, level: {...}}

        Returns:
            <string>success

        Raises:
            Error: parameter incorrect
    """

    # connect to levels.db
    cursor.connect("LEVELS")

    # parse the parameters
    request_data = request.get_data().decode('utf-8')
    updatedData = json.loads(request_data)
    name = json.dumps(updatedData["localization"])
    level = json.dumps(updatedData["clips"])
    id = dict.get(updatedData, "id", "")

    # create or update the level according to level found in database
    if id == "" or cursor.get("ID = " + str(id)) == None:
        cursor.insert("ID, NAME, LEVEL", GenerateID() +
                      ",'" + name + "','" + level + "'")
        print("Created Level")
        return "success"
    else:
        cursor.update(
            "ID = " + str(id),
            "LEVEL = '" + level + "', NAME = '" + name + "'")
        return "success"


@app.route('/level', methods=['DELETE'])
@auth.login_required
def deleteLevel():
    """deletes a level by id

        Call: /level?id=ID_OF_LEVEL

        Returns:
            <string>deleted

        Raises:
            Error: parameter incorrect
    """

    # get the parameter, delete the level if level found, else return "Empty Data"
    id = request.args.get("id")
    if(id == ""):
        return "Empty Data"
    cursor.connect("LEVELS")
    cursor.delete("ID = " + str(id))
    return "deleted"



@app.route('/level', methods=['GET'])
def getLevel(input_ID=None):
    """get level by id    

        Call: /level?id=ID_OF_LEVEL

        Returns:
            level in json string
    """

    # connect to level
    cursor.connect("LEVELS")

    # parse parameters
    if(input_ID):
        id = input_ID
    else:
        id = request.args.get("id")

    level = cursor.get("ID = " + str(id))

    # return level or "Not Found" if level not found
    if level != None:
        print('Level found!')
        return json.dumps(
            {
                'id': level[0],
                'name': level[1],
                'level': level[2]
            })
    return "Not Found"


@app.route('/levels', methods=['GET'])
def getLevels():
    """get all levels' id and 
    level name localization

        Returns:
            levels in json string
    """

    # connect to LEVELS
    cursor.connect("LEVELS")

    # get all levels
    levels = cursor.getAll()

    # parse the levels into json string and returns them
    outputList = []
    for i in range(0, len(levels)):
        outputList.append({
            'id': levels[i][0],
            'localization': levels[i][1]
        })
    return json.dumps(outputList)


@app.route('/image', methods=['POST'])
def uploadImage():
    """upload images for collectibles

        Call: /collectible

        Args: {"id": 00000, "name": collectible_1, collectible: {...}}

        Returns:
            <string>success

        Raises:
            Error: parameter incorrect
    """
    f = request.files['file']
    auth = oss2.Auth('LTAI5tMEmusLKauijzitstYh',
                     'L1BtCwtugHtHjdzC8vpvU531FQceST')
    bucket = oss2.Bucket(
        auth, 'https://oss-cn-beijing.aliyuncs.com', 'eroducate')
    callback_params = {}
    callback_params['callbackUrl'] = 'http://oss-demo.aliyuncs.com:23450'
    callback_params['callbackBody'] = 'bucket=${bucket}&object=${object}'
    callback_params['callbackBodyType'] = 'application/x-www-form-urlencoded'
    encoded_callback = encode_callback(callback_params)
    callback_var_params = {'x:my_var1': 'my_val1', 'x:my_var2': 'my_val2'}
    encoded_callback_var = encode_callback(callback_var_params)
    name = 'Collectible/' + GenerateID() + '.jpg'
    params = {'callback': encoded_callback,
              'callback-var': encoded_callback_var}
    result = bucket.put_object(name, f, params)
    return("https://eroducate.oss-cn-beijing.aliyuncs.com/" + name)


def encode_callback(callback_params):
    cb_str = json.dumps(callback_params).strip()
    return oss2.compat.to_string(base64.b64encode(oss2.compat.to_bytes(cb_str)))


@app.route('/achievement', methods=['POST'])
@auth.login_required
def composeAchievement():
    """creates or updates an achievement   

        Call: /achievement

        Args: {"id": 00000, "name": "achievement_a", achievement: {...}}

        Returns:
            <string>success

        Raises:
            Error: parameter incorrect
    """

    # connect to levels.db
    cursor.connect("ACHIEVEMENTS")

    # parse the parameters
    request_data = request.get_data().decode('utf-8')
    updatedData = json.loads(request_data)
    name = dict.get(updatedData, "name", "")
    condition = dict.get(updatedData, "condition", "")
    serials = json.dumps(updatedData["serials"])
    id = dict.get(updatedData, "id", "")

    # create or update the level according to level found in database
    if id == "" or cursor.get("ID = " + str(id)) == None:
        cursor.insert("ID, NAME, CONDITION, SERIALS", GenerateID() +
                      ",'" + name + "','" + condition + "','" + serials + "'")
        print("Created Achievement")
        return "success"
    else:
        cursor.update(
            "ID = " + str(id),
            "CONDITION = '" + condition + "', SERIALS = '" + serials + "', NAME = '" + name + "'")
        return "success"


@app.route('/achievement', methods=['DELETE'])
@auth.login_required
def deleteAchievement():
    """deletes an achievement by id

        Call: /achievement?id=ID_OF_ACHIEVEMENT

        Returns:
            <string>deleted

        Raises:
            Error: parameter incorrect
    """

    # get the parameter, delete the level if level found, else return "Empty Data"
    id = request.args.get("id")
    if(id == ""):
        return "Empty Data"
    cursor.connect("ACHIEVEMENTS")
    cursor.delete("ID = " + str(id))
    return "deleted"


@app.route('/achievements', methods=['GET'])
def getAchievements():
    '''get all achievements from db'''
    # connect to LEVELS
    cursor.connect("ACHIEVEMENTS")

    # get all levels
    achievements = cursor.getAll()

    # parse the levels into json string and returns them
    outputList = []
    for i in range(0, len(achievements)):
        outputList.append({
            'id': achievements[i][0],
            'name': achievements[i][1],
            'condition': achievements[i][2],
            'serials': achievements[i][3],
        })
    return json.dumps(outputList)

def calculate(x, y, operator):
    '''calculates < > = in string format

    returns the result
    '''
    return x < y if operator == "<" else (x > y if operator == ">" else x == y)


def findSolutionRecursively(valueStack, operatorStack):
    '''
    finds the solution in valueStack and operatorStack
    recursively

    returns the solution as a boolean
    '''
    if len(operatorStack) == 0:
        return reduce(lambda item, result: item and result, valueStack)
    valueStack.insert(0, calculate(valueStack.pop(),
                                   valueStack.pop(), operatorStack.pop()))
    return findSolutionRecursively(valueStack, operatorStack)


def parseCondition(str, score, totalTimesPlayed, supers, middles, fails, levelId):
    '''parse the condition from string to a boolean expression
    and executes it

    returns the result of the expression
    '''

    valueStack = []
    operatorStack = []
    rawStack = str.split(" ")
    phrase = ''

    while len(rawStack) > 0:
        phrase = rawStack.pop()
        if phrase == ">" or phrase == "<" or phrase == "=":
            operatorStack.append(phrase)
        else:
            value = None
            if phrase == "score":
                value = score
            elif phrase == "totalTimesPlayed":
                value = totalTimesPlayed
            elif phrase == "supers":
                value = supers
            elif phrase == "middles":
                value = middles
            elif phrase == "fails":
                value = fails
            elif phrase == "levelId":
                value = levelId
            else:
                value = phrase
            valueStack.append(int(value))
    res = findSolutionRecursively(valueStack, operatorStack)
    return res


@app.route('/achievement', methods=['GET'])
def unlockAhievements():
    '''unlocks ahchievements according to the passing in parameters

    returns a list of unlockable achievements,
    if not achievements available, returns an empty list,
    all in json string format
    '''
    platform = request.args.get("platform")
    score = request.args.get("score")
    totalTimesPlayed = request.args.get("totalTimesPlayed")
    supers = request.args.get("supers")
    middles = request.args.get("middles")
    fails = request.args.get("fails")
    levelId = request.args.get("levelId")

    achievements = json.loads(getAchievements())
    unlocks = []

    for achievement in achievements:
        achievement["serials"] = json.loads(achievement["serials"])
        if parseCondition(achievement["condition"], score, totalTimesPlayed, supers, middles, fails, levelId):
            unlocks.append(achievement["serials"][platform])
    return json.dumps(unlocks)


if __name__ == '__main__':
    # run the up if directly called
    app.run(debug=False)

'''
def initStatsDB():
    achievementCur = sqlite3.connect(
                "achievements.db", check_same_thread=False)
    cursor = achievementCur.cursor()
    cursor.execute('CREATE TABLE ACHIEVEMENTS \
       (ID INT PRIMARY KEY     NOT NULL, \
       NAME          TEXT     NOT NULL, \
       CONDITION           TEXT    NOT NULL, \
       SERIALS           TEXT    NOT NULL); \
       ')
    achievementCur.commit()
    print("Achievement DB initialized")

def initAchievementDB():
    achievementCur = sqlite3.connect(
                "achievements.db", check_same_thread=False)
    cursor = achievementCur.cursor()
    cursor.execute('CREATE TABLE ACHIEVEMENTS \
       (ID INT PRIMARY KEY     NOT NULL, \
       NAME          TEXT     NOT NULL, \
       CONDITION           TEXT    NOT NULL, \
       SERIALS           TEXT    NOT NULL); \
       ')
    achievementCur.commit()
    print("Achievement DB initialized")

def initLevelDB():
    LevelCur.execute('CREATE TABLE LEVELS
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       LEVEL           TEXT    NOT NULL);
       ')
    LevelConnection.commit()
    print("Level DB initialized")

def initUserDB():
    UserCur.execute('CREATE TABLE USERS
       (ID INT PRIMARY KEY     NOT NULL,
       USERNAME           TEXT    NOT NULL,
       PASSWORD           TEXT    NOT NULL);
       ')
    LevelConnection.commit()
    print("User DB initialized")

def initArticleDB():
    ArticleCur.execute(
        'CREATE TABLE ARTICLES(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, ARTICLE TEXT NOT NULL)')
    ArticleConnection.commit()
    print("Article DB initialized")

def initSettingsDB():
    SettingsCur.execute(
        'CREATE TABLE SETTINGS(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, PROP TEXT NOT NULL)')
    SettingsConnection.commit()
    print("Settings DB initialized")
'''
