##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Class used to predict an image file using a yolo model.        #
##################################################################

import darknet

class YoloPredictor:
    CONFIG_PATH = b"yolov3.orig.cfg"
    META_PATH = b"coco.data"

    def __init__(self, weights):
        self.net = darknet.load_net(self.CONFIG_PATH, bytes(weights, encoding='utf-8'), 0)
        self.meta = darknet.load_meta(self.META_PATH)

    def predict_num_cars(self, image_file):
        detection = darknet.detect(self.net, self.meta, bytes(image_file, encoding='utf-8'))
        n_cars = 0

        for object in detection:
            if object[0] == b'car':
                 n_cars += 1

        return n_cars
