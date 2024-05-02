
import os

# Define the desired output path
output_path = '/home/user/videos'  # Or any other path where you have write permissions

# Create the directory with appropriate permissions
os.makedirs(output_path, exist_ok=True)

# Now you should be able to download videos to the specified path
