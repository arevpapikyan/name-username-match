import re
import Levenshtein

def load_nicknames(file_path):
    """
    Loads nicknames from a file and creates a dictionary mapping nicknames to their possible full names.

    Args:
        file_path (str): Path to the nicknames file.

    Returns:
        dict: Dictionary where keys are nicknames and values are lists of possible full names.
    """
    nicknames = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            full_name = parts[0].lower()
            for nickname in parts[1:]:
                nickname = nickname.lower()
                if nickname not in nicknames:
                    nicknames[nickname] = []
                if full_name not in nicknames[nickname]:
                    nicknames[nickname].append(full_name)
    return nicknames

def standardize_name(name, nicknames):
    """
    Standardizes a name by converting it to lowercase and mapping it to full names using the nicknames dictionary.

    Args:
        name (str): The name to standardize.
        nicknames (dict): Dictionary of nicknames to full names.

    Returns:
        list: List of possible full names corresponding to the given name.
    """
    name = name.lower()
    return nicknames.get(name, [name])

def normalize_string(string):
    """
    Normalizes a string by converting it to lowercase and removing non-alphabetical characters.

    Args:
        string (str): The string to normalize.

    Returns:
        str: Normalized string.
    """
    string = string.lower()
    return re.sub(r'[^a-z]', '', string)

def calculate_similarity(name, username):
    """
    Calculates the similarity between two strings using the Levenshtein distance.

    Args:
        name (str): The first string.
        username (str): The second string.

    Returns:
        float: Similarity ratio between the two strings.
    """
    return Levenshtein.ratio(name, username)

def confidence_level(full_name, username, nicknames):
    """
    Calculates the confidence level that a username corresponds to a given full name.

    Args:
        full_name (str): The full name to check.
        username (str): The username to compare.
        nicknames (dict): Dictionary of nicknames to full names.

    Returns:
        str: Confidence level as a percentage string.
    """
    # Normalize the full name and username
    normalized_full_name = normalize_string(full_name)
    normalized_username = normalize_string(username)

    # Split the full name into parts
    name_parts = full_name.lower().split()
    possible_standardized_parts = [standardize_name(part, nicknames) for part in name_parts]

    # Calculate similarity for the full normalized full name against the username
    full_name_similarity = calculate_similarity(normalized_full_name, normalized_username)
    
    # Calculate similarity for each part of the full name with the username
    part_similarities = []
    for standardized_names in possible_standardized_parts:
        part_similarities.append(max(calculate_similarity(part, normalized_username) for part in standardized_names))

    # Consider both the full name similarity and the maximum part similarity
    max_part_similarity = max(part_similarities)
    overall_similarity = max(full_name_similarity, max_part_similarity)
    
    confidence = overall_similarity * 100  # Convert to a percentage
    
    if confidence > 90:
        return f"High confidence: {confidence:.2f}%"
    elif confidence > 60:
        return f"Moderate confidence: {confidence:.2f}%"
    else:
        return f"Low confidence: {confidence:.2f}%"