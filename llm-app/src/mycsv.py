import os
import pathlib
from csv import writer

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")
CSV_FILE = "JOIN_dataset_w_path.csv"

relations = ["""{
  "relations": "
[
    {
        "firstChapter": ["Publication", "Chapter"]
    },
    {
        "bookChapters": ["Publication", "Chapter"]
    }
]"
}""",
"""
{
  "relations": "
[
    {
        "detailedRequirement": ["Requirement", "SpecObject"]
    }
]"
}""",
"""{
  "relations": "
[
    {
        "traces": ["InternalElement", "Event"]
    }""",
"""{
  "relations": "
[
    {
        "specification": ["TraceabilityLink", "Variable"]
    }
]"
}""",
"""{
  "relations": "
[
    {
        "requirements": ["Component", "SpecObject"]
    }
]"
}"""]


with open(CSV_FILE, mode='w', newline='') as csv_file:
    writer1 = writer(csv_file)

    writer1.writerow(['view_description', 'meta_1', 'meta_2', 'relations'])
    i=0
    for folder in os.listdir(VIEWS_DIRECTORY):
        folder_path = os.path.join(VIEWS_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            i += 1
            plant_uml_folder = os.path.join(folder_path, "metamodels", "PlantUML")
            view_description_file = os.path.join(folder_path, "view_description.txt")
            view_description = open(view_description_file, "r").read()
            plant_uml_files =[]
            for file in os.listdir(plant_uml_folder):
                if file.endswith(".txt"):
                    plant_uml_files.append(file)
                    if len(plant_uml_files) == 2:
                        # plantuml1_content = open(plant_uml_files[0], "r").read()
                        # plantuml2_content = open(plant_uml_files[1], "r").read()

                        # Write content to CSV file
                        writer1.writerow([view_description, f"{plant_uml_files[0]}", f"{plant_uml_files[1]}", relations[i-1]])
