prompts = {
    "items": [
        {
            'tags': ['zero-shot'], 
            'template': """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.\
                        Given the following two metamodels and assuming the same domain semantically relates them,\
                        your task is to define which elements can be combined in the final View. In a View, the elements are combined in pairs.\
                        Combining two elements means that the View will include a single element representing the same domain object but combining attributes from each metamodel.
                        Your answer should be a list of elements.\
                        Each element of the list is a dictionary containing the name of this virtual relation and a tuple with the combined elements in the following format: {{Relation_name: (Metamodel_Identifier.Class_name, Metamodel_Identifier.Class_name)}}\
                        Only use class names that actually exist in the metamodels; don't try to invent new class names. The relation's name should combine these class names, always in camelCase.\

                        Metamodel 1: {meta_1}\
                        Metamodel 2: {meta_2}\
                        Relations:""",
        },
    ]
        
}