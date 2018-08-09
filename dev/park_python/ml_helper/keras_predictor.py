##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Class used to predict an image file using a keras model.       #
# It can be used from the command line.                          #
##################################################################

from skimage import io
import keras
from pathlib import Path
import numpy as np
import argparse

class KerasPredictor:
    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)

    def predict_image(self, image):
        return self.model.predict(image.reshape( (1,) + image.shape))

    def predict_images(self, images):
        return self.model.predict(images)

    def predict_image_file(self, image_file):
        image = io.imread(image_file)
        #data = np.array(image)

        return self.predict_image(image)

    def predict_images_path(self, images_path):
        # finding images
        path = Path(images_path)
        
        images = []
        for file in path.iterdir():
            try:
                image = io.imread(file)
                images.append(image)
            except:
                pass
                # doing nothing, the file is just not an image
        
        return self.predict_images(np.array(images))
        

parser = argparse.ArgumentParser("keras predictor")
parser.add_argument("-m", "--model", nargs=1, help="the model file path", type=str, required=True)
parser.add_argument("-i", "--image", nargs=1, help="the image file path to predict", type=str)
parser.add_argument("-p", "--path", nargs=1, help="the path containing the images to predict", type=str)

if __name__ == '__main__':
    args = parser.parse_args()

    predictor = KerasPredictor(args.model[0])

    if args.image != None:
        print(predictor.predict_image_file(args.image[0]))
    elif args.path != None:
        print(predictor.predict_images_path(args.path[0]))
    else:
        print("either an image or a path has to be given")
