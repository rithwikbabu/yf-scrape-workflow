import json

# FILEPATH: /Users/rithwikbabu/Documents/GitHub/SalaryPredictionTransformer/yf-scrape-workflow/test.py

# Load JSON file
with open('old_scraped.json') as file:
    data = json.load(file)

# Calculate average length of text
total_length = 0
count = 0
for value in data:
    total_length += len(value['text'])
    count += 1

average_length = total_length / count if count > 0 else 0
print("Average length of text:", average_length)

