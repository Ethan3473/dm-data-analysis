import data_processing
import data_analysis
import json

def main():
    data = data_processing.load_json("finn_dms.json")
    processed_data = data_processing.extract_processing_info(data, -1)
    print("Processing complete.")

    # word_counts = data_analysis.count_words(processed_data)
    # json.dump(processed_data, open('processed_dms.json', 'w'), indent=4)

    data_analysis.messages_over_time(processed_data)

    
if __name__ == "__main__":
    main()

