import os
import pathlib
from csv import writer

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")
CSV_FILE = "join_dataset.csv"

with open(CSV_FILE, mode='w', newline='') as csv_file:
    writer1 = writer(csv_file)

    writer1.writerow(['user_input', 'meta_1', 'meta_2', 'relations'])

    for folder in os.listdir(VIEWS_DIRECTORY):
        folder_path = os.path.join(VIEWS_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            plant_uml_folder = os.path.join(folder_path, "metamodels", "PlantUML")
            user_input_file = os.path.join(folder_path, "user_input.txt")
            user_input = open(user_input_file, "r").read()
            plant_uml_files =[]
            for file in os.listdir(plant_uml_folder):
                if file.endswith(".txt"):
                    plant_uml_files.append(os.path.join(plant_uml_folder, file))
                    if len(plant_uml_files) == 2:
                        plantuml1_content = open(plant_uml_files[0], "r").read()
                        plantuml2_content = open(plant_uml_files[1], "r").read()

                        # Write content to CSV file
                        writer1.writerow([user_input, f"'{plantuml1_content}'", f"'{plantuml2_content}'"])
