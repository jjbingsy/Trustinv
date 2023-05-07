import re

def parseTitle(string):
    # Search for the first set of alphabet characters and numeric characters
    alphabets = re.search(r'[A-Za-z]+', string)
    numbers = re.search(r'\d+', string)
    
    # Check if both alphabets and numbers are found
    if alphabets and numbers:
        # Create the new string with alphabets, dash, and numbers
        new_string = alphabets.group() + '-' + numbers.group()
        return new_string.upper()
    else:
        # Return an empty string if either alphabets or numbers are not found
        return ''
