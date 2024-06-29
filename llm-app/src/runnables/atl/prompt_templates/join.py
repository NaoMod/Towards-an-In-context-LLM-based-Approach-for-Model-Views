prompts = {
    "items": {
        "zsCoT": {
            'tags': ['ATLjoin-zsCoT'],
            'template': """You are now a PlantUML analyst, finding mapping relations between two different metamodels to help in a ATL transformation development.

                # TASK
                Your task is to analyze the input metamodels and the transformation description and define a list of mappings between the metamodels' classes. 
                It means specifying how source elements from the input metamodel 1 are mapped to target elements in the output metamodel 2.

                # OUTPUT DATA FORMAT
                {format_instructions}

                # RULES
                When generating the response, follow these rules:
                - Only use class names existing in the provided PlantUML metamodels. Don't make them up.
                - The relation's name can be any string, but it must be unique and meaningful for each relation.
                - A relation always contains a from entry (source class) and a to entry (target classes).
                - Each from entry and to entry is named with an alias.
                - A source class can be mapped to multiple target classes, but each target class should be mapped from a single source class.
                - Every class from the input metamodel should be mapped to at least one class in the output metamodel.

                # STEP BY STEP PROCESS
                1. Identify the classes in the input metamodel that need to be transformed into elements in the output metamodel.
                2. Determine the necessary transformations based on the transformation description and input metamodel structure.
                3. Define the logic for transforming elements from the input metamodel into elements in the output metamodel, considering attributes and relationships.
                4. Choose appropriate mapping strategies, such as direct mappings or more complex transformations like 1 to many relations if necessary.
                5. Address any ambiguities or uncertainties in the transformation process.
                6. Create a list of rules containing relations between classes in the input and output metamodels, specifying how elements from the input metamodel are mapped to elements in the output metamodel.

                You can think step-by-step, but your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                Transformation description: {transformation_description}
                Metamodel 1 (input metamodel): {meta_1}
                Metamodel 2 (output metamodel): {meta_2}
                Relations:
                """,
            },
        "1sCoT": {
            'tags': ['ATLjoin-1sCot'], 
            'template': """You are now a PlantUML analyst, finding mapping relations between two different metamodels to help in a ATL transformation development.

                # TASK
                Your task is to analyze the input metamodels and the transformation description and define a list of mappings between the metamodels' classes. 
                It means specifying how source elements from the input metamodel 1 are mapped to target elements in the output metamodel 2.

                # OUTPUT DATA FORMAT
                {format_instructions}

                # RULES
                When generating the response, follow these rules:
                - Only use class names existing in the provided PlantUML metamodels. Don't make them up.
                - The relation's name can be any string, but it must be unique and meaningful for each relation.
                - A relation always contains a from entry (source class) and a to entry (target classes).
                - Each from entry and to entry is named with an alias.
                - A source class can be mapped to multiple target classes, but each target class should be mapped from a single source class.
                - Every class from the input metamodel should be mapped to at least one class in the output metamodel.

                # STEP BY STEP PROCESS
                1. Identify the classes in the input metamodel that need to be transformed into elements in the output metamodel.
                2. Determine the necessary transformations based on the transformation description and input metamodel structure.
                3. Define the logic for transforming elements from the input metamodel into elements in the output metamodel, considering attributes and relationships.
                4. Choose appropriate mapping strategies, such as direct mappings or more complex transformations like 1 to many relations if necessary.
                5. Address any ambiguities or uncertainties in the transformation process.
                6. Create a list of rules containing relations between classes in the input and output metamodels, specifying how elements from the input metamodel are mapped to elements in the output metamodel.

                # EXAMPLE
                Given the following metamodels and transformation description:
                Transformation description: "The transformation will be used to migrate the infomation from the Company to the Corp."
                Metamodel 1:
                @startuml
                title Company

                class Company {{
                    +String name
                }}

                class Employee {{
                    +String name
                    +String position
                }}

                Company --> "0..*" Employee : employs

                @enduml

                Metamodel 2:
                @startuml
                title Corp

                class Corporation {{
                    +String corpName
                }}

                class Worker {{
                    +String workerName
                    +String jobTitle
                }}

                class Freelancer {{
                    +String name
                    +String task
                }}

                Corporation --> "0..*" Worker : hasWorkers

                @enduml

                The result Relations should be:
                {{
                    "relations": [
                        {{
                            "rule": "CompanyToCorporation",
                            "from": {{
                                "c": {{
                                    "metamodel": "Company",
                                    "class": "Company"
                                }}
                            }},
                            "to": {{
                                "corp": {{
                                    "metamodel": "Corp",
                                    "class": "Corporation"
                                }},
                            }}
                        }},
                        {{
                            "rule": "EmployeeToWorker",
                            "from": {{
                                "e": {{
                                    "metamodel": "Company",
                                    "class": "Employee"
                                }}
                            }},
                            "to": {{
                                "w": {{
                                    "metamodel": "Corp",
                                    "class": "Worker",
                                }},
                                "f": {{
                                    "metamodel": "Corp",
                                    "class": "Freelancer",
                                }}
                            }}
                        }}
                    ]
                }}

                You can think step-by-step, but your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                Transformation description: {transformation_description}
                Metamodel 1 (input metamodel): {meta_1}
                Metamodel 2 (output metamodel): {meta_2}
                Relations:
                    """,
        }
    }        
}