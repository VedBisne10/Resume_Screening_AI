import os   # os is used to work with files and folders on the computer


def load_job_descriptions(folder_path):
    # This function loads all job description text files from a given folder
    # and returns them as a dictionary
    # folder_path: the path to the folder containing JD .txt files (e.g. "data/job_descriptions")

    # Create an empty dictionary to store the job descriptions
    # Key = filename (e.g. "JavaDeveloper.txt"), Value = full text content of that file
    # Using filename as key is useful because it becomes the unique ID in ChromaDB
    job_descriptions = {}

    # Loop through every file in the given folder
    for file_name in os.listdir(folder_path):

        # Only process files that end with ".txt" — skip any other file types
        if file_name.endswith(".txt"):

            # Build the complete file path by joining the folder path and filename
            # Example: "data/job_descriptions" + "JavaDeveloper.txt" = "data/job_descriptions/JavaDeveloper.txt"
            file_path = os.path.join(folder_path, file_name)

            # Open the file and read its full content
            # encoding="utf-8" ensures special characters are read correctly
            with open(file_path, "r", encoding="utf-8") as file:

                # Store the file content in the dictionary with the filename as the key
                job_descriptions[file_name] = file.read()

    # Return the dictionary containing all loaded job descriptions
    return job_descriptions
