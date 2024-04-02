import os
import pathlib
from csv import writer

VIEWS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "Views_Baseline")
CSV_FILE = "JOIN_dataset_w_path.csv"

# relations = ["""{
#   "relations": "
# [
#     {
#         "BookPublication": ["Book", "Publication"]
#     },
#     {
#         "ChapterPublication": ["Chapter", "Publication"]
#     }
# ]"
# }""",
# """""",
# """
# {
#   "relations": "
# [
#     {
#         "Attribute": "Attributes"
#     },
#     {
#         "AttributeNameMapping": "FeatureAndClass"
#     },
#     {
#         "Attribute": "Feature"
#     },
#     {
#         "Attribute": "JavaClass"
#     },
#     {
#         "Attribute": "ID"
#     },
#     {
#         "Attribute": "ReferenceValue"
#     },
#     {
#         "Attribute": "Event"
#     },
#     {
#         "AttributeNameMapping": "Log"
#     }
# ]"
# }""",
# """{
#   "relations": "
# [
#     {
#         "combine": ["Abstraction", "Log"]
#     },
#     {
#         "combine": ["Machine", "Trace"]
#     },
#     {
#         "combine": ["Implementation", "Trace"]
#     },
#     {
#         "combine": ["Sees", "Log"]
#     },
#     {
#         "combine": ["Imports", "Log"]
#     },
#     {
#         "combine": ["Values", "Log"]
#     },
#     {
#         "combine": ["ValueExpr", "Trace"]
#     },
#     {
#         "combine": ["ConcreteVariables", "Trace"]
#     },
#     {
#         "combine": ["Variable", "Trace"]
#     },
#     {
#         "combine": ["ConcreteConstants", "Trace"]
#     },
#     {
#         "combine": ["Invariant", "Log"]
#     },
#     {
#         "combine": ["InvariantExpr", "Trace"]
#     },
#     {
#         "combine": ["Type", "Trace"]
#     },
#     {
#         "combine": ["PrimitiveTypeEnum", "VarType"]
#     },
#     {
#         "combine": ["Initialisation", "Log"]
#     },
#     {
#         "combine": ["InitialisationExpr", "Trace"]
#     },
#     {
#         "combine": ["Properties", "Log"]
#     },
#     {
#         "combine"
# }""",
# """{
#   "relations": "
# [
#     {
#         "relationName": ["SpecObject", "Trace"]
#     },
#     {
#         "relationName": ["Specification", "Trace"]
#     },
#     {
#         "relationName": ["SpecRelation", "Trace"]
#     },
#     {
#         "relationName": ["RelationGroup", "Trace"]
#     },
#     {
#         "relationName": ["SpecHierarchy", "Trace"]
#     },
#     {
#         "relationName": ["AttributeDefinition", "Log"]
#     },
#     {
#         "relationName": ["AttributeValue", "Log"]
#     },
#     {
#         "relationName": ["AttributeDefinition", "Exception"]
#     },
#     {
#         "relationName": ["AttributeValue", "Exception"]
#     }
# ]"
# }"""]


with open(CSV_FILE, mode='w', newline='') as csv_file:
    writer1 = writer(csv_file)

    writer1.writerow(['user_input', 'meta_1', 'meta_2', 'relations'])
    i=0
    for folder in os.listdir(VIEWS_DIRECTORY):
        folder_path = os.path.join(VIEWS_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            i += 1
            plant_uml_folder = os.path.join(folder_path, "metamodels", "PlantUML")
            user_input_file = os.path.join(folder_path, "user_input.txt")
            user_input = open(user_input_file, "r").read()
            plant_uml_files =[]
            for file in os.listdir(plant_uml_folder):
                if file.endswith(".txt"):
                    plant_uml_files.append(file)
                    if len(plant_uml_files) == 2:
                        # plantuml1_content = open(plant_uml_files[0], "r").read()
                        # plantuml2_content = open(plant_uml_files[1], "r").read()

                        # Write content to CSV file
                        writer1.writerow([user_input, f"{plant_uml_files[0]}", f"{plant_uml_files[1]}",""])
