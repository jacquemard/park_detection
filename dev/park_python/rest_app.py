##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Main app exposing a REST API. A user can request the root      #
# endpoint to get the current parking state.                     #
# A JSON is sent back to the client:                             # 
# {                                                              #
#     'date':'2018-07-12 12:12:14',                              #
#     'num_cars': 4,                                             #
#     'free_place': 18,                                          #
#     'occupied_rate': 0.432                                     #
# }                                                              #
##################################################################

from flask import Flask, jsonify, request, abort
from time import strftime, gmtime
import pymongo
import datetime
import pytz
import requests
import os
from flask_cors import CORS

MAX_NUM_CARS = 23

TIME_MEAN_SECONDS = 75

VALUES_LENGTH = 20

LOCAL_TIMEZONE = pytz.timezone("Europe/Zurich")

TELEGRAM_KEY = os.environ['TELEGRAM_KEY']

# Database
uri = "mongodb://heig-park:rl5N71ZE5Lvid9MA1lA4O03e7TKDIgA47cuwrcjsN08PAgBrQBrYBOAdPvCqGlHTqbrxHofatBvNoAF0hb9tDQ==@heig-park.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = pymongo.MongoClient(uri)
stats = client['heig-park']['stats']
#stats.create_index([('date', pymongo.ASCENDING)], unique=True)

def current_cars():
    # getting last 4 values from db
    # values = stats.find().sort("date",pymongo.DESCENDING).limit(VALUES_LENGTH)

    # getting last minute from db
    values = stats.find({
        "date":{
            "$gte": datetime.datetime.utcnow() - datetime.timedelta(seconds=TIME_MEAN_SECONDS)
        }
    }).sort("date", pymongo.DESCENDING).limit(VALUES_LENGTH)

    val_sum = 0
    length = 0

    val_date = None
    for value in values:
        val_sum += value['nb_cars']

        if val_date == None or val_date < value['date']:
            val_date = value['date']

        length += 1


    return (round(val_sum / length), val_date)
    
def get_stats():
    db_stats = stats.find().sort("date", pymongo.ASCENDING)
    
    cur_stats = []
    for stat in db_stats:
        cur_stats.append(stat)

    return cur_stats

# firstly loading stats in memory
print("Loading stats")
stats_mem = get_stats()

print("Stats loaded")

def last_date():
    return stats_mem[len(stats_mem) - 1]['date']

def update_stats_mem():
    values = stats.find({
        "date":{
            "$gt":last_date()
        }
    }).sort("date", pymongo.ASCENDING)

    for stat in values:
        stats_mem.append(stat)

@app.route("/")
def route_current():
    cur_num, cur_date = current_cars()

    free_place = MAX_NUM_CARS - cur_num
    if free_place < 0:
        free_place = 0
    
    occupied_rate = (MAX_NUM_CARS - free_place) / MAX_NUM_CARS

    obj = {
        'date':str(cur_date.astimezone(LOCAL_TIMEZONE)),
        'num_cars': cur_num, 
        'free_place': free_place,
        'occupied_rate': occupied_rate
    }
    return jsonify(obj)

app = Flask(__name__)
CORS(app) # Enabling CORS 

@app.route("/stats")
def route_stats():
    # firstly, updating stats_mem
    update_stats_mem()

    #db_stats = stats.find().sort("date", pymongo.DESCENDING)

    # stats per 10 minute only
    cur_stats = []
    index = 0
    for stat in stats_mem:
        if index % VALUES_LENGTH == 0:
            cur_stats.append({
                "date": str(stat["date"].astimezone(LOCAL_TIMEZONE)),
                "nb_cars": stat["nb_cars"]
            })
        index += 1

    return jsonify(cur_stats)

@app.route("/bot", methods=["POST"])
def telegram_bot_updates():
    print("Telegram update received")
    print(request.get_json())
    body = request.get_json()['message']
    text = body['text']

    # /status command
    if text.startswith('/status'):
        # sending a response to the user 
        chat_id = body['chat']['id']

        cur_num, cur_date = current_cars()

        cur_date = cur_date.astimezone(LOCAL_TIMEZONE)

        free_place = MAX_NUM_CARS - cur_num
        if free_place < 0:
            free_place = 0
        
        #occupied_rate = (MAX_NUM_CARS - free_place) / MAX_NUM_CARS

        msg = "Il y a actuellement {0} voitures présentes, pour environ {1} places libres. Statut au {2}.".format(cur_num, free_place, cur_date.strftime("%d.%m.%y à %H:%M"))

        dict_msg = {
            "chat_id": chat_id,
            "text": msg
        }

        requests.post("https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_KEY), dict_msg)        

    if text.startswith('/start'):
        # sending a response to the user 
        chat_id = body['chat']['id']

        msg = "Salut! Tape '/status' pour avoir des infos sur le parking de la HEIG-VD !"

        dict_msg = {
            "chat_id": chat_id,
            "text": msg
        }

        requests.post("https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_KEY), dict_msg)     

    return '', 200


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
