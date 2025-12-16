import json

def load_json(file_path):
    """" Loads JSON data from a file. """

    with open(file_path, 'r', encoding = "utf-8") as file:
        raw_data = json.load(file)

    data = raw_data.get("messages")

    return data


def extract_processing_info(data, limit = -1):
    """ Extracts relevant information from the data and saves it to a new JSON file. """

    processed_data = []
    counter = 0

    for entry in data:
        if counter < limit or limit == -1:
            if entry.get("content") != "":
                processed_data.append({
                    "sender": (entry.get("author")).get("nickname"),
                    "timestamp": entry.get("timestamp"),
                    "message": entry.get("content")
                })
                counter += 1
    
    json.dump(processed_data, open('processed_finn_dms.json', 'w'), indent=4)


def count_words(data):
    """ Count the total number of times each word is used in the dataset for each user. """

    messages = []
    
    for entry in data:
        messages.append({entry.get("sender"): entry.get("content")})
    
    user_word_counts = []

    for message in messages:
        for sender in message.keys():
            word_dictionary = {}

            for content in message.items(): # Get sender and content
                words = content.lower().split() # Split content into list of lower case words

                for word in words: # Calibrate word counts
                    if word not in word_dictionary:
                        word_dictionary[word] = 1
                    else:
                        word_dictionary[word] += 1

            sender_words = {sender: word_dictionary}
            user_word_counts.append(sender_words)

    return user_word_counts