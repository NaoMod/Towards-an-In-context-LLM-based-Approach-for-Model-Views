prompts = {
    "items": {
        "zsCoT": {
            'template': """You are now a PlantUML analyst that find relations between classes from two metamodels.
                        
                        # TASK
                        Your task is to analyze the input metamodels and the view description and define a list of relations between the metamodels' classes.
                        The classes are always combined in pairs, being one coming from the first metamodel and the other coming from the second metamodel.
                        Classes can be combined when they represent the same domain object or when they are complementary classes, which means that one can be extended with the attributes of the other.

                        Other possible reason for combinations is when the view description includes explicit attribbutes from one metamodel that should appear in the other.
                                                
                        Each relation always contains precisely one class coming from each metamodel.
                        In your response, the classes are always in order: the first class comes from the first metamodel, and the second class comes from the second metamodel.

                        # OUTPUT DATA FORMAT                        
                        {format_instructions}                     
                       
                        # RULES
                        When generating the JSON response, you should follow these rules:
                        - Only use class names that exist in the metamodels. Never include classes that are not in the metamodels
                        - The relation's name can be any string, but it should be unique and meaningful for each relation.

                        # STEP BY STEP PROCESS
                        1. Identify all the classes from the first metamodel.
                        2. Identify all the classes from the second metamodel.
                        3. Given the metamodels and their classes, combine the elements in pairs when the selected classes represent the same domain object in each metamodel.
                        4. Given the metamodels and their classes, combine the elements in pairs when some selected class in the second metamodel can be complemented by some chosen class on the first metamodel and vice-versa.
                        5. Analyse the view description to find out other potential relations.
                        6. Ensure that the classes are combined in pairs, one from each metamodel.
                        7. Ensure that the relation's name is unique and meaningful.
                        8. Ensure that all the classes exist in the PlantUML metamodels.
                        9. Create the JSON array with the combination pairs.
                        10. Provide the answer.               

                        You can think step-by-step, but your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                        # INPUT
                        View description: {view_description}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        Relations:""",
        },
        "1sCoT": {
            'template': """You are now a PlantUML analyst that find relations between classes from two metamodels.
                        
                        # TASK
                        Your task is to analyze the input metamodel and the view description and define a list of relations between the metamodels' classes.
                        The classes are always combined in pairs, being one coming from the first metamodel and the other coming from the second metamodel.
                        Classes can be combined when they represent the same domain object or when they are complementary classes, which means that one can be extended with the attributes of the other.

                        Other possible reason for combinations is when the view description includes explicit attribbutes from one metamodel that should appear in the other.
                                                
                        Your answer should be a valid JSON list of dictionaries where each dictionary entry represents a relation. 
                        It should be a list even when it contains just one relation.
                        Each relation always contains precisely one class coming from each metamodel.
                        In your response, the classes are always in order: the first class comes from the first metamodel, and the second class comes from the second metamodel.

                        # OUTPUT DATA FORMAT                        
                        {format_instructions}                       
                       
                        # RULES
                        When generating the JSON response, you should follow these rules:
                        - Only use class names that exist in the metamodels. Never include classes that are not in the metamodels
                        - The relation's name can be any string, but it should be unique and meaningful for each relation.

                        # STEP BY STEP PROCESS
                        1. Identify all the classes from the first metamodel.
                        2. Identify all the classes from the second metamodel.
                        3. Given the metamodels and their classes, combine the elements in pairs when the selected classes represent the same domain object in each metamodel.
                        4. Given the metamodels and their classes, combine the elements in pairs when some selected class in the second metamodel can be complemented by some chosen class on the first metamodel and vice-versa.
                        5. Analyse the view description to find out other potential relations.
                        6. Ensure that the classes are combined in pairs, one from each metamodel.
                        7. Ensure that the relation's name is unique and meaningful.
                        8. Ensure that all the classes exist in the PlantUML metamodels.
                        9. Create the JSON array with the combination pairs.
                        10. Provide the answer.

                        # EXAMPLE
                        Given the following metamodels and view description:
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

                        The result Relations should be:
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
                

                        You can think step-by-step, but your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                        # INPUT
                        View description: {view_description}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        Relations:""",
        }
    }        
}