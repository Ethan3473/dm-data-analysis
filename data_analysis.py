import matplotlib.pyplot as plt
import pandas as pd

def count_words(data):
    """ Count the total number of times each word is used in the dataset for each user. """

    user_word_counts = {}
    
    for entry in data:
        sender = entry["sender"]
        message = entry["message"]

        if sender not in user_word_counts:
            user_word_counts[sender] = {}
        
        words = message.lower().split()

        for word in words:
            user_word_counts[sender][word] = user_word_counts[sender].get(word, 0) + 1

    for sender in user_word_counts:
        user_word_counts[sender] = dict(
            sorted(
                user_word_counts[sender].items(),
                key = lambda item:item[1],
                reverse = True
            )
        )

    return user_word_counts

def messages_over_time(data):
    """ Maps messages sent over time by each user, pandas confuses the hell out of me """

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc = True, format="ISO8601") # Convert weird date formatting to readable times

    counts = df.set_index("timestamp").groupby("sender").resample("M").size() # Makes timestamp the index, splits into a table for each sender, chops time into monthly brackets using new index, count how many rows in each sender month bracket

    counts = counts.reset_index() # Reset index to boring 0, 1, ...
    counts = counts.rename(columns={0: "count"})

    counts["month"] = counts["timestamp"].dt.strftime("%Y-%m") # Create new month column by formatting old timestamp column nicely
    users = counts["sender"].unique()
    months = counts["month"].unique() 
    tick_positions = range(0, len(months), 2)

    fig, axes = plt.subplots(len(users), 1, sharex=True, figsize = (18, 6)) # Creates a figure with the number of subplots that there are users, shares their x ticks, axes = list of subplots 

    for ax, user in zip(axes, users): 
        user_data = counts[counts["sender"] == user] # Check if counts["sender"] is user. Pandas gets rows that are true
        ax.bar(user_data["month"], user_data["count"]) # Set x to the months, set y to message count
        ax.set_title(user)
        ax.set_ylabel("Messages")

    axes[-1].set_xticks(tick_positions)
    axes[-1].set_xticklabels(months[::2])

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    return 