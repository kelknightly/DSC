import os
import re
import pandas as pd
from textblob import TextBlob

def extract_info_from_filename(filename):
    match = re.match(r'DSC(\d{2})(\d{2})-(.+)\.txt', filename)
    if match:
        return match.groups()
    return None

def clean_character_field(character):
    # Removing specific phrases in square brackets
    return re.sub(r'\[.*?\]', '', character).strip()

def sentiment_analysis(directory_path):
    all_data = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            season, episode, title = extract_info_from_filename(filename)
            file_path = os.path.join(directory_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if ':' in line:
                        parts = line.split(':', 1)
                        character = clean_character_field(parts[0])
                        dialogue = parts[1].strip()
                        sentiment = TextBlob(dialogue).sentiment.polarity
                        all_data.append([season, episode, title, character, dialogue, sentiment])

    return all_data

# Directory containing the text files
directory_path = r'C:\Users\kellt\projects\dsc-sentiment-analysis'  

# Run sentiment analysis
data = sentiment_analysis(directory_path)

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=['Season', 'Episode', 'Title', 'Character', 'Dialogue', 'Sentiment Score'])
csv_file_path = 'star_trek_discovery_season_1_sentiment_analysis.csv'
df.to_csv(csv_file_path, index=False)

print(f"Sentiment analysis completed. Data saved to {r'C:\Users\kellt\projects\dsc-sentiment-analysis'}")
