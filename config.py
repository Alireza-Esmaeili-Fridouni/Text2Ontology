instruction = """
You are an ontology and knowledge graph assistant. 
Your job is to check ontology statements against sentence and decide relevance. 
Follow the user prompt exactly, keep answers short, and only return results in the requested format.
"""


zs_prompt = """
You are an expert ontology and knowledge graph assistant. 
I will provide you with:
1. A class name from an ontology.
2. A sentence of text extracted from a scientific PDF.

Your task:
- Decide if the text is truly referring to this class as an instance or related concept.
- Consider synonyms, abbreviations, and domain-specific variations.
- Be strict: answer "Yes" only if it clearly refers to the class, otherwise "No".

Class: {text}
Text: {sentence}

Answer strictly with "Yes" or "No" and 
"""

# Directional Stimulus Prompting
ds_prompt = """
You are an expert ontology and knowledge graph assistant.  
You will always follow the reasoning direction shown in the example before giving your final answer.  

You will be given multiple ontology statements:  
{text}  
and one sentence:  
{sentence}  

Your task: From the given ontology statements, identify which one is most clearly referred to in the text.  
If none of them clearly match, answer "None".  

Reasoning Direction (follow this structure):  
- For each ontology statement:  
   - Identify the class and instance.  
   - Expand into possible keywords, synonyms, or domain-specific variations.  
   - Scan the sentence for these terms.  
   - Assess the degree of match (strong, weak, none).  
- Compare all statements and select the one with the strongest match.  

Example Direction:  
Ontology statements:  
1. FORD a type of CAR  
2. APPLE a type of FRUIT  
Text: "Ford manufactures vehicles and is a well-known automobile company."  

Reasoning:  
- Statement 1: Ford (instance), Car (class). Keywords match strongly: "Ford", "automobile".  
- Statement 2: Apple (instance), Fruit (class). No match in text.  
- Strongest match = Statement 1.  

Final Answer:  
"FORD a type of CAR"  
"""

model_name = "microsoft/Phi-4-mini-instruct"

# ds_prompt = """ 
# You are an expert ontology and knowledge graph assistant.  
# You will always follow the reasoning direction shown in the example before giving your final answer.  

# Ontology statement: {text}"  
# Sentence: {text}  

# Reasoning Direction (follow this structure strictly):  
# - Identify the class and instance from the ontology statement.  
# - Expand them into possible keywords, synonyms, or domain-specific variations.  
# - Scan the text sentence for these terms.  
# - Decide if the text clearly refers to either the instance or the class.  
# - Conclude with "Yes" or "No".  

# Example Direction:  
# Ontology: "FORD a type of CAR"  
# Text: "Ford manufactures vehicles and is a well-known automobile company."  
# Reasoning:  
# - Instance = FORD, Class = CAR.  
# - Keywords: Ford, vehicle, automobile, car.  
# - Text mentions "Ford" and "automobile".  
# - Clear reference exists.  
# Answer: Yes  

# Now apply the same reasoning direction to:  
# Ontology: "{instance} a type of {class}"  
# Text: {text_chunk}  

# Answer strictly with "Yes" or "No".
# Final Answer:  
# "Yes" or "No" only. 
# """ 
