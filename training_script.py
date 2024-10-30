import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import Image
from numpy import asarray

'''
commands in the terminal

#!git clone https://github.com/ultralytics/yolov5
#!cd yolov5/ & git pull 
#!cd yolov5 & pip install -r requirements.txt
'''


#detection before training

#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', autoshape=False)

img = r"dataset_creating\undistorted_dataset_cropping\56.png"
#img2 = r"datasets\tableobjects\train\images\WhatsApp-Video-2023-12-18-at-09_44_34_c58a1a04_mp4-33_jpg.rf.d08bb727b98f29da186e2d69515411aa.jpg"

#results.print()
#print(results.pandas().xywh[0])
#results.show()

'''
commands in terminal

!python train.py --img 640 --batch 4 --epochs 25 --data polygons.yaml --weights yolov5s.pt

'''

#detection after training

#model_trained = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp6/weights/best.pt')

#detect_results = model_trained('datasets/polygons/test/images/56_undistorted.png')

#detect_results.show()