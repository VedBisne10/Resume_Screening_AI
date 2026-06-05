import os

def load_job_descriptions(folder_path):
    # Dictionary to store job descriptions
    # Using a dictionary because it stores the data as key:value pair ("python_developer.txt": "Python Developer\nPython\nDocker\nAWS") and becomes a unique ID stored in chromaDB
    job_descriptions = {}   

    # Loop through all files present in the given folder
    for file_name in os.listdir(folder_path):

        # Process only text files (.txt) containing job descriptions
        if file_name.endswith(".txt"):  

            # Create the complete path of the file  
            file_path = os.path.join(
                folder_path,
                file_name
            )

            # Open the file in read mode using UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as file:
                
                # Read the entire file content and store it using the filename as the dictionary key
                job_descriptions[file_name] = file.read()

    return job_descriptions