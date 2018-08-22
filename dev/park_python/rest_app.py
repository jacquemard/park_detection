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

MAX_NUM_CARS = 23

TIME_MEAN_SECONDS = 75

VALUES_LENGTH = 4

LOCAL_TIMEZONE = pytz.timezone("Europe/Zurich")



# Database
uri = "mongodb://heig-park:rl5N71ZE5Lvid9MA1lA4O03e7TKDIgA47cuwrcjsN08PAgBrQBrYBOAdPvCqGlHTqbrxHofatBvNoAF0hb9tDQ==@heig-park.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = pymongo.MongoClient(uri)
stats = client['heig-park']['stats']


def current_cars():
    # getting last 4 values from db
    # values = stats.find().sort("date",pymongo.DESCENDING).limit(VALUES_LENGTH)

    # getting last minute from db
    values = stats.find({
        "date":{
            "$gte": datetime.datetime.utcnow() - datetime.timedelta(seconds=TIME_MEAN_SECONDS)
        }
    }).sort("date",pymongo.DESCENDING).limit(VALUES_LENGTH)

    val_sum = 0
    length = 0

    val_date = None
    for value in values:
        val_sum += value['nb_cars']

        if val_date == None or val_date < value['date']:
            val_date = value['date']

        length += 1


    return (round(val_sum / length), val_date)
    


app = Flask(__name__)

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

@app.route("/stats")
def route_stats():
    db_stats = stats.find().sort("date")

    cur_stats = []
    for stat in db_stats:
        cur_stats.append({
            "date": str(stat["date"].astimezone(LOCAL_TIMEZONE)),
            "nb_cars": stat["nb_cars"]
        })

    return jsonify(cur_stats)

@app.route("/bot", methods=["POST"])
def telegram_bot_updates():
    #print(request.get_json())
    body = request.get_json()
    text = body['text']

    # /status command
    if text.startswith('/status'):
        # sending a response to the user 
        chat_id = body['chat']['id']

        cur_num, cur_date = current_cars()

        free_place = MAX_NUM_CARS - cur_num
        if free_place < 0:
            free_place = 0
        
        #occupied_rate = (MAX_NUM_CARS - free_place) / MAX_NUM_CARS

        msg = "Il y a actuellement {0} voitures présentes, pour environ {1} places libres. Statut au {2}.".format(cur_num, free_place, cur_date.strftime("%d.%m.%y à %H:%M"))

        dict_msg = {
            "chat_id": chat_id,
            "text": msg
        }

        requests.post("https://api.telegram.org/bot625265830:AAEYwsQ9tD0KrDAkC-EW5NGydWkpo1VyVq4/sendMessage", dict_msg)        

    if text.startswith('/start'):
        # sending a response to the user 
        chat_id = body['chat']['id']

        msg = "Tape '/status' pour avoir des infos sur le parking de la HEIG-VD !"

        dict_msg = {
            "chat_id": chat_id,
            "text": msg
        }

        requests.post("https://api.telegram.org/bot625265830:AAEYwsQ9tD0KrDAkC-EW5NGydWkpo1VyVq4/sendMessage", dict_msg)     

    return '', 200

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
