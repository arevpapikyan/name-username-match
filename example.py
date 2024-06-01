import functions

# Load nicknames from the provided file
nicknames = functions.load_nicknames("nicknames.txt")

# Example dictionary of names and usernames
name_username_dict = {
    "John Doe": "johndoe123",
    "Elizabeth Smith": "liz_smith",
    "Robert Johnson": "bob_j",
    "Mary Jane": "maryjane456",
    "Michael Brown": "mike_b",
    "Mike Brown": "mike_b",
    "Emily Davis": "emilydavis789",
    "Ab Johnson": "absalom_j"
}

# Loop through each name-username pair and calculate confidence level
for name, username in name_username_dict.items():
    confidence = functions.confidence_level(name, username, nicknames)
    print(f"Confidence level for {name} and {username}: {confidence}")
