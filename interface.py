import tkinter as tk
import data_processing
import data_analysis
from tkinter import messagebox
import json


class app():
    """ Load the interface and its components """
    def __init__(self):
        self.root = tk.Tk()
        self.load_data_text = tk.StringVar()
        self.loaded_data = {}
        self.processed_data = {}
        self.process_limit = -1
        self.counted_messages = {}

        heading = tk.Label(self.root, text = "DM data processing and visualisation", font = ('calibre', 15, 'bold'))
        heading.grid(row = 0, column = 0)

        load_data_label = tk.Label(self.root, text = "Enter JSON name:")
        load_data_label.grid(row = 1, column = 0)

        load_data_path = tk.Entry(self.root, textvariable = self.load_data_text)
        load_data_path.grid(row = 2, column = 0)

        load_data_button = tk.Button(self.root, text = "Load JSON", command = self.load_data_clicked, width = 15)
        load_data_button.grid(row = 2, column = 1)

        process_data_label = tk.Label(self.root, text = "Set entry process count (default = all):")
        process_data_label.grid(row = 3, column = 0)

        process_data_limit = tk.Entry(self.root, textvariable = self.process_limit)
        process_data_limit.grid(row = 4, column = 0)

        process_data_button = tk.Button(self.root, text = "Process", command = self.process_data_clicked, width = 15)
        process_data_button.grid(row = 4, column = 1)

        messages_count_label = tk.Label(self.root, text = "Count different messages for all users:")
        messages_count_label.grid(row = 5, column = 0)

        messages_count_button = tk.Button(self.root, text = "Count", command = self.messages_count_clicked, width = 15)
        messages_count_button.grid(row = 6, column = 0)

        self.root.geometry("800x400")
        self.root.title("DM data processing and visualisation")

        self.root.mainloop()


    def load_data_clicked(self):
        """ Runs when JSON submitted """
        file_path = self.load_data_text.get()

        if not file_path.endswith(".json"):
            file_path += ".json"

        try:
            self.loaded_data["data"] = data_processing.load_json(file_path)
            messagebox.showinfo("Success", "File successfully loaded")

        except FileNotFoundError:
            messagebox.showwarning("Error", "Invalid file name")
        return
    

    def process_data_clicked(self):
        """ Call process data function with processed data """

        try:
            self.processed_data = data_processing.extract_processing_info(self.loaded_data["data"], self.process_limit)
            messagebox.showinfo("Success", "JSON successfully processed")
        
        except KeyError:
            messagebox.showwarning("Error", "No JSON loaded")
        return


    def messages_count_clicked(self):
        """ Run the messages count function using loaded data """

        if self.processed_data != {}:
            self.counted_messages = data_analysis.count_words(self.processed_data)
            json.dump(self.counted_messages, open('dm_message_counts.json', 'w'), indent=4)
            messagebox.showinfo("Success", "Message counts successfully output")

        else:        
            messagebox.showwarning("Error", "No processed data found")