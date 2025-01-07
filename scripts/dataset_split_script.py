
import os
import shutil
from sklearn.model_selection import train_test_split

#paths for images and labels
images_dir = r"dataset_creating\final_dataset\images"
labels_dir = r"dataset_creating\final_dataset\labels"

split_folder = r"datasets\polygons"

#output directories for splits
output_dirs = {
    "train": {"images": os.path.join(split_folder, "train/images"), "labels": os.path.join(split_folder, "train/labels")},
    "val": {"images": os.path.join(split_folder, "val/images"), "labels": os.path.join(split_folder, "val/labels")},
    "test": {"images": os.path.join(split_folder, "test/images"), "labels": os.path.join(split_folder, "test/labels")},
}

#output directories if they don't exist
for split in output_dirs:
    for key in output_dirs[split]:
        os.makedirs(output_dirs[split][key], exist_ok=True)

#list all image files and corresponding label files
image_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]
label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]

# Split dataset into training, validation, and test sets
train_images, test_images, train_labels, test_labels = train_test_split(image_files, label_files, test_size=0.3)
val_images, test_images, val_labels, test_labels = train_test_split(test_images, test_labels, test_size=0.5)

#helper function to copy images and labels
def copy_files(images, labels, split_name):
    for img_file, lbl_file in zip(images, labels):
        shutil.copy2(os.path.join(images_dir, img_file), output_dirs[split_name]["images"])
        shutil.copy2(os.path.join(labels_dir, lbl_file), output_dirs[split_name]["labels"])

#copy files to each split directory
copy_files(train_images, train_labels, "train")
copy_files(val_images, val_labels, "val")
copy_files(test_images, test_labels, "test")

