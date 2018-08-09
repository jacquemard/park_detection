##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Helper methods to handle the PKLot dataset                     #
# When called from the command line, PKLot xmls can be convert   #
# to VOC xml files.                                              #
##################################################################

from pathlib import Path
import os
import sys
cur_path = Path(os.path.abspath(__file__) )
lib_path = str(cur_path.parent.parent.resolve())
sys.path.insert(0, lib_path)

import numpy as np
import math
from lxml import etree
from xml.etree import ElementTree
import argparse
import camera.image_processing as process



def get_cars_grid(image_size, grid_size, xml_file):
    # parsing the xml
    tree = etree.parse(xml_file)

    # finding cars
    cars = tree.xpath("/parking/space[@occupied='1']/rotatedRect/center")
    
    # 2D array representing the grid
    grid = np.zeros((grid_size, grid_size))

    # dimension of a cell
    cell_dim = (math.ceil(image_size[0] / grid_size), math.ceil(image_size[1] / grid_size))

    # mapping the cars to the grid
    for car in cars:
        pixel_x, pixel_y = (int(car.attrib['x']), int(car.attrib['y']))
        grid_x, grid_y = (math.floor(pixel_x / cell_dim[1]), math.floor(pixel_y / cell_dim[0]))

        grid[grid_y][grid_x] = 1.0

    return grid

'''
def get_cars_grid_no_padding(image_size, grid_size, xml_file):
    # parsing the xml
    tree = etree.parse(xml_file)

    # finding cars
    cars = tree.xpath("/parking/space[@occupied='1']/rotatedRect/center")
    
    # 2D array representing the grid
    grid = np.zeros((grid_size, grid_size))

    # dimension of a cell
    cell_dim = (math.floor(image_size[0] / grid_size), math.floor(image_size[1] / grid_size))

    # mapping the cars to the grid
    for car in cars:
        pixel_x, pixel_y = (int(car.attrib['x']), int(car.attrib['y']))
        grid_x, grid_y = (math.floor(pixel_x / cell_dim[1]), math.floor(pixel_y / cell_dim[0]))

        grid[grid_y][grid_x] = 1.0

    return grid
'''


def count_cars(xml_file):
    # parsing the xml
    tree = etree.parse(xml_file)

    # counting cars
    cars = tree.xpath("/parking/space[@occupied='1']")
    return len(cars)

def images_with_xml(dataset_path):
    IMAGE_EXT = ".jpg"
    images = [ 
        (os.path.join(root, f), os.path.join(root, f[:-len(IMAGE_EXT)] + ".xml"))
        for root, _, files in os.walk(dataset_path) 
        for f in files 
        if f.endswith(IMAGE_EXT)]

    return images

def processed_images_with_xml(dataset_path):
    IMAGE_EXT = "_processed.bmp"
    images = [ 
        (os.path.join(root, f), os.path.join(root, f[:-len(IMAGE_EXT)] + ".xml"))
        for root, _, files in os.walk(dataset_path) 
        for f in files 
        if f.endswith(IMAGE_EXT)]

    return images

def xml_to_voc(xml_file, xml_output_file):
    IMAGE_SHAPE = (720, 1280, 3)
    # parsing the xml
    tree_in = etree.parse(xml_file)

    # creating xml VOC file
    root = ElementTree.Element("annotation")
    # -- filename
    filename = Path(xml_file).name
    filename_elem = ElementTree.Element("filename")
    filename_elem.text = filename[:-len(".xml")] + ".jpg"
    root.append(filename_elem)

    # -- size
    height = IMAGE_SHAPE[0]
    width = IMAGE_SHAPE[1]
    depth = IMAGE_SHAPE[2]

    size_elem = ElementTree.Element("size")
    root.append(size_elem)
    width_elem = ElementTree.Element("width")
    width_elem.text = str(width)
    size_elem.append(width_elem)
    height_elem = ElementTree.Element("height")
    height_elem.text = str(height)
    size_elem.append(height_elem)
    depth_elem = ElementTree.Element("depth")
    depth_elem.text = str(depth)
    size_elem.append(depth_elem)

    # -- segmented
    segmented_elem = ElementTree.Element("segmented")
    segmented_elem.text = str(0)
    root.append(segmented_elem)

    # -- cars
    contours = tree_in.xpath("/parking/space[@occupied='1']/contour")  
    for contour in contours:
        # finding points
        xmin = width
        ymin = height
        xmax = ymax = 0
        for point in contour:
            # updating bounding box
            x = int(point.get("x"))
            y = int(point.get("y"))

            if x < xmin:
                xmin = x
            if y < ymin:
                ymin = y
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y
        
        # adding element
        object_element = ElementTree.Element("object")
        root.append(object_element)

        name_elem = ElementTree.Element("name")
        name_elem.text = "car"
        object_element.append(name_elem)

        bounds_elem = ElementTree.Element("bndbox")
        object_element.append(bounds_elem)

        xmin_elem = ElementTree.Element("xmin")
        xmin_elem.text = str(xmin)
        bounds_elem.append(xmin_elem)
        ymin_elem = ElementTree.Element("ymin")
        ymin_elem.text = str(ymin)
        bounds_elem.append(ymin_elem)
        xmax_elem = ElementTree.Element("xmax")
        xmax_elem.text = str(xmax)
        bounds_elem.append(xmax_elem)
        ymax_elem = ElementTree.Element("ymax")
        ymax_elem.text = str(ymax)
        bounds_elem.append(ymax_elem)

    tree_out = ElementTree.ElementTree(root)
    tree_out.write(xml_output_file)

def xmls_to_tensorflow_api(xml_path, xml_output_path):
    #xml_output_path = annotations_path + "/xmls"
    # creating the trainval text file
    #trainval_file = open(annotations_path + "/trainval.txt", "w")

    # finding xmls 
    for root, _, files in os.walk(xml_path):
        for filename in files:
            if filename.endswith(".xml"):
                file = os.path.join(root, filename)
                # creating voc files
                xml_to_voc(file, xml_output_path + "/" + filename)
                # Adding the image to trainvals
                #trainval_file.write(file.split('.')[-1] + "\n")


    #trainval_file.close()



parser = argparse.ArgumentParser("pklot dataset helper")
parser.add_argument("-i", "--input", nargs=1, help="the path to the xmls to parse", type=str, required=True)
parser.add_argument("-o", "--output", nargs=1, help="the path to the xmls output foler", type=str, required=True)

if __name__ == '__main__':
    args = parser.parse_args()

    xml_path = args.input[0]
    xml_output_path = args.output[0]

    xmls_to_tensorflow_api(xml_path, xml_output_path)