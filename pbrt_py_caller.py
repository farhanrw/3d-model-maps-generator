# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math  
import re
import csv
import numpy as np

def tensorGenerator(phi, theta):
    filename = "materials_phi_"+ str(phi) + "_theta_" + str(theta) + ".txt"
    parsed_filename = "materials_phi_"+ str(phi) + "_theta_" + str(theta) + ".csv"
    with open(filename) as f:
        content = f.readlines()
        content = [x.strip() for x in content] 
    return parsed_filename, content
# you may also want to remove whitespace characters like `\n` at the end of each line

def convertToCSV():
    for i in range(1, 90, 10):
        print("Progress",(i*100)/17)
        for j in range(1, 360, 20):
                parsed_filename, rough_tensors = tensorGenerator(i, j)
                parsed_tensors = []
                for element in rough_tensors:
                    element = re.sub('[\[\]\(\)\{\}<>]', '', element)
                    element = re.sub('[  ]', '', element)
                    element = re.sub('[,]', ',', element)
                    element = element.split(",")
                    
                    parsed_tensors.append(np.array(element, dtype=np.float32))
                    # with open(parsed_filename, mode='a+') as tensor_inter:
                    #     tensor_writer = csv.writer(tensor_inter, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    #     tensor_writer.writerow(element)
                np.savetxt('test1.txt', np.array(parsed_tensors), fmt='%f')

def getPhi(x, y, z):
    return math.atan2(math.sqrt(x*x + z * z), y)

def getTheta(x, y, z):
    return math.atan2(x, -z)


def getRadius(x, y, z):
    return math.sqrt(x*x + y * y + z * z)

def getX(radius, theta, phi):
    #std::cout << std::endl << std::endl << radius * sin(phi*0.01745) * cos(theta*0.01745) << " ::: theta is " << theta << "phi is" << phi << "radius is " << radius << std::endl;
    return radius * math.sin(phi*0.01745) * math.cos(theta*0.01745);


def getY(radius, theta, phi):
    return radius * math.sin(phi*0.01745) * math.sin(theta*0.01745);


def getZ(radius, theta, phi):
    return radius * math.cos(phi*0.01745);

def generateCameraPoses():
    radius = 290 #default = 210 in dataset
    camera_poses = []
    for phi in range(90, 91, 2000):
        for theta in range(130, 360, 2500):
            camera_poses.append([getX(radius, theta, phi), getY(radius, theta, phi), getZ(radius, theta, phi), phi, theta])
    return camera_poses            
    
def getOnePose(camera_list, index):
    return camera_list[index]

cam_poses = generateCameraPoses()

from tqdm import tqdm

for i in tqdm(range(len(cam_poses))):
    cam_pos = cam_poses[i]
    cf = open("camera.pbrt", "w+")
    ff = open("film.pbrt", "w+")
    cf.write("LookAt ")
    cf.write("%f %f %f\n0 0 0\n0 1 0" % (cam_pos[0], cam_pos[2], cam_pos[1]))
    ff.write("Film \"image\" \"string filename\" \"try/pred_phi_%s_theta_%s.png\" \"integer xresolution\" [400] \"integer yresolution\" [400]" %  (str(cam_pos[3]), str(cam_pos[4])) )
    cf.close()
    ff.close()
    os.system(r"/home/farhan/Masters_Thesis/pbrt-v3/cmake-build-release/pbrt --quiet --nthreads=16 thesis.pbrt")
    #os.rename("face_writer.txt", "data_phi_%s_theta_%s.txt" %  (str(cam_pos[3]), str(cam_pos[4])))
    
    
