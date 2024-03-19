prompts = {
    "items": [
         {
            'tags': ['where-zsCot'], 
            'template': """You specialize in reason on PlantUML metamodels, especially combining and merging them.
                        
                        Given two metamodels, a list of relations that contains classes from each one, and a user input, your task is to define how to combine them.
                        
                        It means you need to define the combination rules to combine elements from both metamodels.
                        
                        For the input relations list, you may assume the following template between the delimiter <relations>:

                        <relations>
                        [
                            {{
                                "relationName": ["class_name_of_first_metamodel", "class_name_of_second_metamodel"]
                            }}
                        ]
                        </relations>
                        
                        Your final answer will be a JSON array representing a list of combination rules.
                        
                        For the output, you should provide a JSON array with the combination rules per relation following the template:

                        <combinations>
                            [
                                {{
                                    "relationName": {{
                                        "rule": "Metamodel_Identifier.Class_name.Attributte {{combination_rule}} Metamodel_Identifier.Class_name.Attributte"
                                    }}
                                }}
                            ]
                        </combinations>
                        
                        Each rule is in the following format: Metamodel_Name.Class_name.Attributte {{combination_rule}} Metamodel_Name.Class_name.Attributte
                        
                        When generating the JSON text:
                        Only use class and attribute names that actually exist in the metamodels. Don't make them up.
                        The combination_rule can be one of the following: equal, different, greater, less, greaterOrEqual, lessOrEqual, contains, issubstringof.
                        The combination_rule should be chosen according to the semantics of the domain. 
                        
                        The step-by-step process is as follows:

                        1. Select the metamodels to be analyzed for each relation in the list of relations.
                        2. For each pair of metamodel classes, analyze the domain considering the user's needs and elaborate a possible combination to relate both classes.
                        3. Create the JSON array with the combination for each relation.
                        5. Provide the final answer.

                        Your final answer should contain only the valid JSON and nothing else. Exclude any explanation or delimiter from the final response.

                        User input: {user_input}
                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}
                        List of relations: {relations}

                        Combination rules:"""
        },
        {
            'tags': ['zero-shot'], 
            'template': """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.
                        Given the following two metamodels, your task is to define how to combine them.
                        It means you need to define the combination rules to combine elements from both metamodels.
                        Your answer should be a list of combination rules.
                        Each rule is in the following format: Metamodel_Identifier.Class_name.Attributte {{combination_rule}} Metamodel_Identifier.Class_name.Attributte
                        Only use class and attribute names that actually exist in the metamodels; don't try to invent new names.
                        The combination_rule can be one of the following: equal, different, greater, less, greaterOrEqual, lessOrEqual.
                        The combination_rule should be chosen according to the semantics of the domain. 

                        Metamodel 1: {meta_1}
                        Metamodel 2: {meta_2}

                        combination rules:"""
        },
    ]
        
}