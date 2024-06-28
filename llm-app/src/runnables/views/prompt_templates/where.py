prompts = {
    "items": {
         "zsCoT": {
            'tags': ['where-zsCoT'],
            'template': """You specialize in reason on PlantUML metamodels, especially combining and merging them.
                        
                        Given two metamodels, a list of relations containing classes' pairs, and a view description, your task is to define how to combine the given classes.
                                                
                        It means you must define the combination rules to combine classes from both metamodels.
                                                
                        For the input relations list, you may assume the following template:

                        {{
                            "relations": [
                                {{
                                    "name": "relationName",
                                    "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                                }}
                            ]
                        }}
                                                                                               
                        {format_instructions}
                                                                    
                        When generating the response text you should follow these rules:
                        Only use class and attribute names that actually exist in the metamodels. Don't make them up.
                        The combination_rule should be a string explaining how the classes can be connected according to the domain's semantics. It means explaining what kind of comparisons can be used to connect the classes in the relation.
                                                
                        The step-by-step process is as follows:

                        1. Select the metamodels to be analyzed for each relation in the list of relations.
                        2. For each pair of metamodel classes, analyze the domain considering the view description and elaborate a possible combination to relate both classes.
                        3. Create the JSON array with the combination rule for the relation. The combination rule is a list  that constains the name of the first metaclass, the combination explanation and the name of the second metaclass.
                        4. Create the JSON array with one rule per relation.
                        5. Provide the final answer.

                        Exclude any explanation or delimiter from the final response.

                        View description: {view_description}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        List of relations: {join}
                        Combination rules:""",
         },
         "1sCoT": {
            'tags': ['where-1sCot'], 
            'template': """You specialize in reason on PlantUML metamodels, especially combining and merging them.
                        
                        Given two metamodels, a list of relations containing classes' pairs, and a view description, your task is to define how to combine the given classes.
                                                
                        It means you must define the combination rules to combine classes from both metamodels.
                                                
                        For the input relations list, you may assume the following template:

                        {{
                            "relations": [
                                {{
                                    "name": "relationName",
                                    "classes": ["class_name_from_first_metamodel", "class_name_from_second_metamodel"]
                                }}
                            ]
                        }}
                                                                                               
                        {format_instructions}
                                                                    
                        When generating the response text you should follow these rules:
                        Only use class and attribute names that actually exist in the metamodels. Don't make them up.
                        The combination_rule should be a string explaining how the classes can be connected according to the domain's semantics. It means explaining what kind of comparisons can be used to connect the classes in the relation.
                                                
                        The step-by-step process is as follows:

                        1. Select the metamodels to be analyzed for each relation in the list of relations.
                        2. For each pair of metamodel classes, analyze the domain considering the view description and elaborate a possible combination to relate both classes.
                        3. Create the JSON array with the combination rule for the relation. The combination rule is a list  that constains the name of the first metaclass, the combination explanation and the name of the second metaclass.
                        4. Create the JSON array with one rule per relation.
                        5. Provide the final answer.

                        # Example
                        Given the following metamodels, relations and view description:
                        View description: "The view  should conatins the name, and email from the Customer and also the name of the item bought by they."
                        Metamodel 1:
                        @startuml

                            class Customer {{
                                +int id
                                +String name
                                +String email
                                +String deliveryAddress
                            }}

                            @enduml
                        Metamodel 2:
                        @startuml

                            class Item {{
                                +int id
                                +String name
                                +String category
                            }}

                            class Order {{
                                +int orderId
                                +String orderNumber
                                +Date orderDate
                                +Date creationDate
                                +String currentOrderStatus
                                +String customerName
                            }}

                            @enduml
                        List of relations:
                        {{
                            "relations": [
                                {{
                                    "name": "itemBoughtByCustomer",
                                    "classes": [
                                        "Customer",
                                        "Item"
                                    ]
                                }}
                            ]
                        }}

                        The result of Combination rules should be:
                        {{
                        "rules": [
                            {{
                                "name": "itemBoughtByCustomer",
                                "rules": [
                                    "The customerName of Order should be equal to the name of the Customer that bought the Item"
                                ]
                            }}
                        ]
                       }}

                        Exclude any explanation or delimiter from the final response.

                        View description: {view_description}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        List of relations: {join}
                        Combination rules:"""
        }
    }        
}
