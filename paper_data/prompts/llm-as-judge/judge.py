prompts = {
    "items": {
        "judge": {
            'template': """[Instruction]
                            Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below. For this evaluation, you should primarily consider the following criteria:
                            helpfulness: The given input is a view description that should be specified using the VPDL language. 
                            Given that, how much effort would someone who knows the domain, the underlying metamodels and the VPDL languange syntax need to make to get the prediction to match the reference? 
                            The less effort needed, the higher the score.
                            You should consider the VPDL language syntax, the metamodels, and the domain knowledge to evaluate the response, but you can ignore the where part.
                            
                            [Ground truth]
                            {{original_vpdl}}

                            Begin your evaluation by providing a short explanation. Be as objective as possible. After providing your explanation, you must rate the response on a scale of 1 to 10 by strictly following this format: "[[rating]]", for example: "Rating: [[5]]".

                            [Question]
                            {{view_description}}

                            [The Start of Assistant's Answer]

                            {{generated_vpdl}}

                            [The End of Assistant's Answer]
                    """,
        }
    }        
}