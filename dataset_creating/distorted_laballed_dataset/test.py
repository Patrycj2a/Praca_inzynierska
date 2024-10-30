import os
# specify the directory path
dir_path = r"C:\Users\Pati\Desktop\STUDIA_AIR\III_rok\VI_semestr\Inzynierka\dataset\undistorted_dataset_cropping"

# loop through all files in the directory
for filename in os.listdir(dir_path):

    # check if the file is a text file
    if filename.endswith(".png"):

        # construct the old file path
        old_file_path = os.path.join(dir_path, filename)

        file_name = os.path.splitext(filename)[0]

        # construct the new file name
        new_file_name = f"{file_name}_undistorted.png"

        # construct the new file path
        new_file_path = os.path.join(dir_path, new_file_name)

        os.rename(old_file_path, new_file_path)