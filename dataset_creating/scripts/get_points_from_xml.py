import xml.etree.ElementTree as ET
import cv2
import numpy as np
from numpy import load
import os

#load calibration data
data = load(r"dataset_creating\kalibracja\calibration.npz")
lst = data.files

cam_calib_matrix = data['mtx'] #camera calibration matrix
dist_coeff = data['dist'] #distortion coefficients
r_vectors = data['rvecs'] #rotation vectors
t_vectors = data['tvecs'] #translation vectors



#load xml data 
tree = ET.parse(r"dataset_creating\distorted_laballed_dataset\annotations.xml")
root = tree.getroot()



#function to undistort a list of points from xml file

def points_undistortion(points, calib_matrix, dist_coefficients, new_camera_matrix) -> np.array:
    #convert points into the required shape for cv2.undistortPoints (N,1,2)
    points_array = np.array(points, dtype=np.float32).reshape(-1, 1, 2)

    #undistort the points with the new camera matrix - return normalized points
    undistorted_points = cv2.undistortPoints(points_array, calib_matrix, dist_coefficients, new_camera_matrix)

    #undistorted points back to pixel units - normalized are very small
    pixel_undistorted_points = cv2.perspectiveTransform(undistorted_points, calib_matrix) #calib_matrix

    #convert to array
    pixel_undist_points_array = pixel_undistorted_points.reshape(-1, 2)

    return pixel_undist_points_array



#calculate new camera matrix

def calculate_optimal_camera_matrix(img_shape: np.array, calib_matrix, dist_coeffs) -> tuple[np.array, np.array]:
    shape = (img_shape[1], img_shape[0])
    new_shape = (img_shape[1], img_shape[0])
    return cv2.getOptimalNewCameraMatrix(calib_matrix, dist_coeffs, shape, 1, new_shape)


img_shape = np.array([1920,1200])
new_camera_mtx, roi = calculate_optimal_camera_matrix(img_shape, cam_calib_matrix, dist_coeff)


#create a directory to store the text files, if it doesn't exist
output_dir = "undistorted_points"
os.makedirs(output_dir, exist_ok=True)

#initialize a dictionary to store the points for each image
undistorted_images = {}

for image in root.findall('.//image'):
    image_name = image.attrib['name']  #get the image name

    output_filename = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}_undistorted.txt")

    undistorted_polygons = {}

    #open file to make some changes in it
    with open(output_filename, 'w') as file:

        #find all <polygon> elements within the <image> tag
        for polygon in image.findall('.//polygon'):
            label = polygon.attrib['label']  #get the label attribute (e.g., osmiokat, szesciokat)
            points = polygon.attrib['points']  #get the points attribute
            point_list = [tuple(map(float, point.split(','))) for point in points.split(';')]  #convert to list of tuples

            #undistort points
            undistorted_points = points_undistortion(point_list, cam_calib_matrix, dist_coeff, new_camera_mtx) 
            undistorted_polygons[label] = undistorted_points #store points in a dictionary with the label as the key

            #write points to file
            file.write(f"{label} {undistorted_points}")

        
        undistorted_images[image_name] = undistorted_polygons

'''
---print the extracted, undistorted points with image name and label

for image_name, undistorted_polygons in undistorted_images.items():
    print(f"Image: {image_name} ")
    for label, points in undistorted_polygons.items():
        print(f"Undistorted {label}: {points}")
'''
