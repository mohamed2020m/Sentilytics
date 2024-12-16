import re

def clean_unicode_escape(text):
    # Replace all unicode escape sequences like \u003c with their corresponding characters
    cleaned_text = re.sub(r'\\u[0-9a-fA-F]{4}', lambda match: chr(int(match.group()[2:], 16)), text)
    
    # You can extend this step if you want to remove specific characters like '<' or '>'
    # For now, we just remove characters like '<' or '>'
    cleaned_text = cleaned_text.replace('<', '').replace('>', '')
    
    return cleaned_text

# Example usage
data = "Neo-Liberalism \u003e Anarcho-Capitalism \u003e Feudalist Capitalism , Welcome to the New Dark Ages!\nPeople that bought into this are exactly the cattle figures Milei likes to drive."
cleaned_data = clean_unicode_escape(data) 
print(cleaned_data)
