import os
import pathlib
from csv import writer

ATL_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_ATL_Baseline")
CSV_FILE = "ATL_dataset.csv"

# Open the CSV file for writing
with open(CSV_FILE, mode='w', newline='') as csv_file:
    writer1 = writer(csv_file)

    # Write the header row to the CSV file
    writer1.writerow(['transformation_description', 'meta_1', 'meta_2'])

    i = 0
    for folder in os.listdir(ATL_DIRECTORY):
        folder_path = os.path.join(ATL_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            i += 1
            metamodel_folder = os.path.join(folder_path, "metamodels")
            transformation_description_file = os.path.join(folder_path, "transformation_description.txt")

            # Read the transformation description
            transformation_description = open(transformation_description_file, "r").read()

            # List to hold .ecore files
            ecore_files = []
            for file in os.listdir(metamodel_folder):
                if file.endswith(".ecore"):
                    ecore_files.append(file)
                    if len(ecore_files) == 2:
                        # Write content to CSV file
                        writer1.writerow([transformation_description, ecore_files[0], ecore_files[1]])