import imageio.v2 as imageio # type: ignore
import imgaug as ia  # type: ignore
from imgaug import augmenters as iaa   # type: ignore
from imgaug.augmentables.polys import Polygon, PolygonsOnImage  # type: ignore
import numpy as np
import re, os, cv2
import matplotlib as plt


#load polygon points fro txt file content
def load_polygon_points_with_labels(file_path: str) -> dict[str, list[tuple[float, float]]]:
    with open(file_path, 'r') as f:
        file_content = f.read()

    #regular expression to capture the label and corresponding polygon points
    matches = re.findall(r'(\w+)\s+\[\[(.*?)\]\]', file_content, re.DOTALL)

    polygons_with_labels = {}
    
    #process each match (label and array of points)
    for match in matches:
        label = match[0]  #extract the label (e.g., osmiokat, szesciokat, etc.)
        array_str = match[1]  #extract the string representation of the points
        
        #replace any brackets or extra spaces
        array_str = re.sub(r'[\[\]]', '', array_str.strip())

        #split by spaces or commas to extract all the numbers
        points = re.split(r'[,\s]+', array_str.strip())

        #convert to a NumPy array and reshape to (n, 2)
        array = np.array([float(p) for p in points if p]).reshape(-1, 2)

        #convert np array back to list of tuples (for augmenting polygons)
        point_list_of_tuples = [tuple(point) for point in array]

        polygons_with_labels.setdefault(label, [])

        #add the polygon points under the corresponding label - key, it stores multiple values under one key
        polygons_with_labels[label].append(point_list_of_tuples)

    
    return polygons_with_labels



#additional functions for visualising the polygons on image - sligthly moved because of int() operation which is a must when visualize 

def visualize_augmented_polygons(image_aug: np.ndarray, psoi_aug: ia.PolygonsOnImage) -> None:
    for i, poly in enumerate(psoi_aug.polygons):
        print(poly)
        #get the list of points from the augmented polygon
        points = [(point[0], point[1]) for point in poly.exterior]

        #convert the list of points into a numpy array (required by OpenCV)
        points_np = np.array(points, dtype=np.float32)
        
        #assign a unique color for each label (random color generation)
        color = tuple(np.random.randint(0, 255, 3).tolist())
        points_np_int = np.round(points_np).astype(np.int32)
        
        #draw the polygon on the augmented image
        cv2.polylines(image_aug, [points_np_int], isClosed=True, color=color, thickness=2)
        

    #display the image with augmented polygons
    cv2.imshow('Augmented Image with Polygons', image_aug)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def visualize_polygons_on_image(image: np.ndarray, polygons_with_labels: dict[str, list[tuple[float, float]]]) -> None:
    for label, polygons in polygons_with_labels.items():
        for polygon in polygons:
            points_np = np.array(polygon, dtype=np.int32)
            cv2.polylines(image, [points_np], isClosed=True, color=(0, 0, 255), thickness=2)

    cv2.imshow('Original Image with Polygons', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#augumentation
def augumentation(image_path: str, polygons_with_labels: dict[str, list[tuple[float, float]]], img_name: str) -> None:
    #load single image
    image = cv2.imread(image_path)

    labels = []
    Polygons = []

    for label, polygons in polygons_with_labels.items():
        for polygon in polygons:
            labels.append(label)
            Polygons.append(Polygon(polygon))

    #convert polygons to an PolygonsOnImage instance
    psoi = ia.PolygonsOnImage(Polygons, shape=image.shape)
    
    #Sometimes(0.5, ...) applies the given augmenter in 50% of all cases,
    #e.g. Sometimes(0.5, GaussianBlur(0.3)) would blur roughly every second image.
    sometimes_15 = lambda aug: iaa.Sometimes(0.15, aug)
    sometimes_25 = lambda aug: iaa.Sometimes(0.25, aug)
    sometimes_35 = lambda aug: iaa.Sometimes(0.35, aug)
    sometimes_50 = lambda aug: iaa.Sometimes(0.5, aug)

    #augumentation
    aug = iaa.Sequential(
    [
        #apply the following augmenters to the images
        sometimes_15(iaa.GaussianBlur(sigma= (0.0, 2.0))),
        sometimes_25(iaa.SaltAndPepper(0.1)),
        sometimes_35(iaa.CropAndPad(
            percent= (-0.15, 0.15),
            pad_mode=["constant", "edge"]
            )),
        sometimes_50(iaa.Affine(
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-45, 45)
        ))
    ],
    random_order=True
)

    image_aug, psoi_aug = aug(image=image, polygons=psoi)
    
    output_dir = "augumented_images_labels"

    #ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #save the augmented image as a .png file
    augmented_img_path = os.path.join(output_dir, f"{img_name}_aug.png")
    cv2.imwrite(augmented_img_path, image_aug)

    #save the augmented polygon points into a .txt file
    augmented_txt_path = os.path.join(output_dir, f"{img_name}_aug.txt")

    #mapping from class names to class IDs
    class_to_id = {
        "czworokat": 0,
        "szesciokat": 1,
        "osmiokat": 2,
        "dwunastokat": 3
    }
    
    with open(augmented_txt_path, 'w') as f:

        for i, poly in enumerate(psoi_aug.polygons):
            #polygon converted to list of point tuples
            tuple_list = [(point[0], point[1]) for point in poly.exterior]
            

            #iterate thrpugh each x, y coordinate in polygon and get the extreme values min max
            x_points = [point[0] for point in tuple_list]
            y_points = [point[1] for point in tuple_list]

            #coordinates of the bounding box
            min_x = np.min(x_points)
            max_x = np.max(x_points)
            min_y = np.min(y_points)
            max_y = np.max(y_points)

            width = max_x - min_x
            height = max_y - min_y

            img_shape = np.array([1920,1200])

            #normalized yolo format coordinates
            x_center = np.round(((max_x + min_x) / 2) / img_shape[0], 8)
            y_center = np.round(((max_y + min_y) / 2) / img_shape[1], 8)
            w = np. round(width / img_shape[0], 8)
            h = np. round(height / img_shape[1], 8)

            #getting label name and convert it to the corresponding ID
            label_name = labels[i]
            label_id = class_to_id.get(label_name) 
            
            
            #writing the ID and normalized coordinates to the file
            f.write(f"{label_id} {x_center} {y_center} {w} {h}\n")

    #visualisation to check results on the image

    #visualize_augmented_polygons(image, psoi)


def iterate_all_images_and_poligons(image_folder: str, polygons_folder: str) -> None:
    image_files = os.listdir(image_folder)


    #iterate through each image of the images folder
    for image_file in image_files:

        #extract the image name (without extension) to match with the polygon file
        #if I want to run again this function I have to adjust the code because now the image is called 1_undistorted.png
        image_name = os.path.splitext(image_file)[0]

        #build the path to the corresponding polygon file
        polygon_file_path = os.path.join(polygons_folder, f"{image_name}.txt") #undistorted points

        #load polygon points from the file
        if os.path.exists(polygon_file_path):
            polygons_with_labels = load_polygon_points_with_labels(polygon_file_path) #return dict undistorted points with labels

            #build full path to the image for the next argument
            image_path = os.path.join(image_folder, image_file)

            augumentation(image_path, polygons_with_labels, image_name)


#function to format undistorted points for original images to yolo format (above only augumented points were formatted so had to add it)
def yolo_point_formatting(polygons_undistorted_folder: str):

    polygons_files = os.listdir(polygons_undistorted_folder)

    #sort files ascending, so to get polygons in the correct order the same as files
    #sorted_files = sorted(image_files, key=lambda x: int(re.search(r'\d+', x).group()))

    #iterate through each image of the images folder
    for polygons_file in polygons_files:

        #extract the image name (without extension) to match with the polygon file
        #if I want to run again this function I have to adjust the code because now the image is called 1_undistorted.png
        file_name = os.path.splitext(polygons_file)[0]

        #build the path to the corresponding polygon file
        polygon_file_path = os.path.join(polygons_undistorted_folder, f"{file_name}.txt")

        #load polygon points from the file
        if os.path.exists(polygon_file_path):
            polygons_with_labels_undistorted = load_polygon_points_with_labels(polygon_file_path) #return dict points with labels


            output_dir = r"dataset_creating\final_dataset\labels"

            #save the formatted polygon points into a .txt file
            formatted_txt_path = os.path.join(output_dir, f"{file_name}.txt")

            #mapping from class names to class IDs
            class_to_id = {
                "czworokat": 0,
                "szesciokat": 1,
                "osmiokat": 2,
                "dwunastokat": 3
            }
            
            with open(formatted_txt_path, 'w') as f:

                for label, polygons in polygons_with_labels_undistorted.items():
                    for polygon in polygons:
                        #polygon converted to list of point tuples
                        tuple_list = [(point[0], point[1]) for point in polygon]
                        

                        #iterate thrpugh each x, y coordinate in polygon and get the extreme values min max
                        x_points = [point[0] for point in tuple_list]
                        y_points = [point[1] for point in tuple_list]

                        #coordinates of the bounding box
                        min_x = np.min(x_points)
                        max_x = np.max(x_points)
                        min_y = np.min(y_points)
                        max_y = np.max(y_points)

                        width = max_x - min_x
                        height = max_y - min_y

                        img_shape = np.array([1920,1200])

                        #normalized yolo format coordinates
                        x_center = np.round(((max_x + min_x) / 2) / img_shape[0], 8)
                        y_center = np.round(((max_y + min_y) / 2) / img_shape[1], 8)
                        w = np. round(width / img_shape[0], 8)
                        h = np. round(height / img_shape[1], 8)

                        #getting label name and convert it to the corresponding ID
                        label_id = class_to_id.get(label) 
                        
                        
                        #writing the ID and normalized coordinates to the file
                        f.write(f"{label_id} {x_center} {y_center} {w} {h}\n")

#execute function - testing