##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Used to validate a tensorflow model over a dataset.            #
# The number of cars predicted and wanted are written within a   #
# csv file.                                                      #
##################################################################

import sys
import os
from pathlib import Path
cur_path = Path(os.path.abspath(__file__) )
lib_path = str(cur_path.parent.parent.resolve())
sys.path.insert(0, lib_path)

from tensorflow_api_predictor import TensorflowPredictor
from skimage import io
from dataset_helper import pklot

IMAGES_PATH = "/home/ubuntu/DS/PKLot/tensorflow_ds/images_splitted/test"
IMAGE_EXT = ".jpg"
MODEL_PATH = "../final_models/tensorflow/pklotfull_16000_frozen_graph.pb"
RESULT_PATH = "pklotfull_16000_eval.csv"
XMLS_PATH = "/home/ubuntu/DS/PKLot/tensorflow_ds/annotations/xmls"

predictor = TensorflowPredictor(MODEL_PATH)
result = open(RESULT_PATH, "w")

for root, _, files in os.walk(IMAGES_PATH):
    for f in files:
        if f.endswith(IMAGE_EXT):
            path = os.path.join(root, f)
            image = io.imread(path)

            xml_filename = f[:-len(IMAGE_EXT)] + ".xml"
            xml = os.path.join(XMLS_PATH, xml_filename)

            n_cars = predictor.predict_num_cars(image)
            real_n_cars = pklot.count_cars(xml)

            result.write("{},{}\n".format(n_cars, real_n_cars))
            print("{} - predicted: {}, wanted:{}".format(f, n_cars, real_n_cars))

result.close()
