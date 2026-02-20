# Example Usage of extract_tcga_subtypes Module

# Import the necessary module
from extract_tcga_subtypes import extract_subtypes

# Sample data
sample_data = [
    {'sample_id': 'TCGA-AO-1234', 'data': {'some_feature': 'value1'}},
    {'sample_id': 'TCGA-AB-5678', 'data': {'some_feature': 'value2'}}
]

# Using the extract_subtypes function
subtypes = extract_subtypes(sample_data)

# Printing the output
print("Extracted Subtypes:", subtypes)