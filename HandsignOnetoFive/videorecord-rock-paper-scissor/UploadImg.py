import os
import concurrent.futures
from roboflow import Roboflow

# Initialize the Roboflow object with your API key
rf = Roboflow(api_key="TcaLNZLqMGI3J22Lccon")

# Specify workspace and project IDs
workspaceId = 'kickhands'
projectId = 'rock-paper-scissor-if71v'

# Access the workspace and project
workspace = rf.workspace(workspaceId)
project = workspace.project(projectId)

# Specify the folder containing your images
folder_path = "C:\\Skripsi\\YoloCodeNotebook\\HandsignOnetoFive\\frame-rock-paper-scissor"

# Get a list of all image files in the folder (only jpg images)
image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

# Sort the files based on the numeric part of the filenames (e.g., frame1, frame2, etc.)
image_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

# Set the total number of images in the sequence
sequence_size = len(image_files)

# Function to upload a single image
def upload_image(image_file, index):
    image_path = os.path.join(folder_path, image_file)

    # Set the sequence number based on the index (1-based numbering)
    sequence_number = index + 1  # 1-based index, so first image gets sequence_number 1

    # Upload the image with sequence number and sequence size
    try:
        project.upload(
            image_path=image_path,  
            batch_name="rock-paper-scissor",  
              
            num_retry_uploads=3,  
            tag_names=["YOUR_TAG_NAME"],  
            sequence_number=sequence_number,  
            sequence_size=sequence_size  # Set the total number of images in the sequence
        )
        print(f"[{image_path}] was uploaded successfully with sequence number {sequence_number}.")
    except Exception as e:
        print(f"Failed to upload {image_file}: {e}")

# Use ThreadPoolExecutor to upload images in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Submit all the image uploads to the executor
    futures = [executor.submit(upload_image, image_file, index) for index, image_file in enumerate(image_files)]

    # Wait for all the uploads to complete
    concurrent.futures.wait(futures)
