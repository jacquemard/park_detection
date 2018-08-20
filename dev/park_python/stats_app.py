##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
##################################################################

from pathlib import Path
import os
import sys
cur_path = Path(os.path.abspath(__file__))

from camera.capture import CameraClient, CameraAgent
from ml_helper.tensorflow_api_predictor import TensorflowPredictor
from skimage import io
from time import gmtime, strftime
import pymongo
import datetime

CAMERA_HOST = "ipcam.einet.ad.eivd.ch"
USERNAME = "admin"
PASSWORD = "Lfg3hgPhLdNYW"

MODEL_FILE = str(cur_path.parent.resolve()) + "/final_models/tensorflow/pklotfull_4000_frozen_graph.pb"

MAX_NUM_CARS = 23

VALUES_LENGTH = 4

# Creating a camera client
camera = CameraClient(CAMERA_HOST, USERNAME, PASSWORD)

# Creating the tensorflow predictor
predictor = TensorflowPredictor(MODEL_FILE)

# Database
uri = "mongodb://heig-park:rl5N71ZE5Lvid9MA1lA4O03e7TKDIgA47cuwrcjsN08PAgBrQBrYBOAdPvCqGlHTqbrxHofatBvNoAF0hb9tDQ==@heig-park.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = pymongo.MongoClient(uri)
stats = client['heig-park']['stats']

def add_db_value(value):
    obj = {
        "date": datetime.datetime.utcnow(),
        "nb_cars": value
    }

    obj_id = stats.insert_one(obj).inserted_id
    print("{} cars, stored within database with id {}".format(obj["nb_cars"], obj_id))


def image_received(image):
    image = io.imread(image)
    num_cars = predictor.predict_num_cars(image)
    print("image received, num_car: {}".format(num_cars))
    add_db_value(num_cars)

agent = CameraAgent(camera, image_received, seconds=15, blocking=True)
agent.start()
