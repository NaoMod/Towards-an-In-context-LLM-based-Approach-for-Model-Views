prompts = {
    "items": [
        {
            'tags': ['zero-shot'], 
            'template': """You are a computer program specialized in reason on PlantUML metamodels, especially combining and merging them into objects called Views.\
                        Given the following two metamodels, your task is to define how to combine them.\
                        It means you need to define the conditions to combine elements from both metamodels.\
                        Your answer should be a list of conditions.\
                        Each condition is in the following format: Metamodel_Identifier.Class_name.Attributte {{combination_rule}} Metamodel_Identifier.Class_name.Attributte\
                        Only use class and attribute names that actually exist in the metamodels; don't try to invent new names.\
                        The combination_rule can be one of the following: equal, different, greater, less, greaterOrEqual, lessOrEqual.\
                        The combination_rule should be chosen according to the semantics of the domain. \

                        Metamodel 1: {meta_1}\
                        Metamodel 2: {meta_2}\

                        Conditions:"""
        },
    ]
        
}