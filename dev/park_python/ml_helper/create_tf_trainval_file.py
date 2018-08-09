##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Used to create a trainval file for the tensorflow library from #
# a folder. Each images within it add a line to the trainval     #
# file.                                                          #
##################################################################

import os

def create_trainval_file(input_path, ext, output_file):
     # creating the trainval text file
    trainval_file = open(output_file, "w")

    for _, _, files in os.walk(input_path):
        for f in files:
            if f.endswith(ext):
                # Adding the image to trainvals
                trainval_file.write(f.split('.')[-2] + "\n")
    trainval_file.close()
