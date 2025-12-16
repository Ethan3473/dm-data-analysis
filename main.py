import data_processing

def main():
    data = data_processing.load_json("finn_dms.json")
    data_processing.extract_processing_info(data, 2000)
    print("Processing complete.")

if __name__ == "__main__":
    main()

