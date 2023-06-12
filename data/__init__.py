
"""init prompt data"""
import json

"""Load App example data"""
with open('data/example.json', 'r') as f:
    example = json.load(f)

"""Load prompt data"""
with open('data/prompt.json', 'r') as f:
    prompt_text = json.load(f)['prompt_text']
