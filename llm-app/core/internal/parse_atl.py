import os
import json
import re
import pathlib
# This code is not part of the main application. It should be used to extra processing the VPDL and ATL files.
def parse_atl_file(file_path):
    relations = []
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Regex pattern to match rule definitions and their associated classes in ATL files
        rule_pattern = re.compile(r'rule\s+(\w+)\s*\{\s*from\s+(.+?)\s*to\s+(.+?)\s*\}', re.DOTALL)
        class_pattern = re.compile(r'(\w+)\s*:\s*([^!]+)!(\w+)')
        
        rules = rule_pattern.findall(content)
        for rule in rules:
            rule_name = rule[0]
            from_classes = class_pattern.findall(rule[1])
            to_classes = class_pattern.findall(rule[2])
            
            from_classes_dict = {cls[0]: {'metamodel': cls[1], 'class': cls[2]} for cls in from_classes}
            to_classes_dict = {cls[0]: {'metamodel': cls[1], 'class': cls[2]} for cls in to_classes}
            
            relations.append({
                'rule': rule_name,
                'from': from_classes_dict,
                'to': to_classes_dict
            })
    
    return relations

def process_folders(base_folder):
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            atl_file = None
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.atl'):
                    atl_file = os.path.join(folder_path, file_name)
                    break
            if atl_file:
                relations = parse_atl_file(atl_file)
                json_file_path = os.path.join(folder_path, 'relations.json')
                with open(json_file_path, 'w') as json_file:
                    json.dump({'relations': relations}, json_file, indent=4)
                print(f'Processed folder: {folder_name}')

if __name__ == "__main__":
    base_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "..", "..", "Views_ATL_Baseline")
    process_folders(base_folder)
