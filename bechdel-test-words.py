import re
import os
import glob
import pandas as pd
from collections import Counter

def collect_bechdel_passing_words(file_path, gender_dict):
    dialogue_pattern = re.compile(r'^([A-Z][A-Z\s\']*):\s*(.*)')

    words = []
    prev_character = None
    prev_dialogue = ""

    with open(file_path, 'r') as file:
        for line in file:
            match = dialogue_pattern.match(line)
            if match:
                character, dialogue = match.groups()
                character = character.strip().upper()

                if gender_dict.get(character) == 'Female':
                    if prev_character and prev_character != character:
                        combined_dialogue = prev_dialogue + " " + dialogue
                        if not re.search(r'\b(he|him|his|man|men|guy|guys|boy|boys)\b', combined_dialogue, re.IGNORECASE):
                            dialogue_words = re.findall(r'\w+', combined_dialogue.lower())
                            words.extend(dialogue_words)
                    prev_character = character
                    prev_dialogue = dialogue

    return words

def main():
    gender_dict = {
        'BURNHAM': 'Female', 'GEORGIOU': 'Female', 'TILLY': 'Female', 'DETMER': 'Female', 
        'OWOSEKUN': 'Female', "T'RINA": 'Female', 'CORNWELL': 'Female', 'COMPUTER': 'Female',
        "L'RELL": 'Female', 'PSYCHO': 'Female', 'DRAKE': 'Female', 'STELLA': 'Female',
        'AMANDA': 'Female', 'NARWANI': 'Female', 'DENNAS': 'Female', 'AIRIAM': 'Female',
        'POLLARD': 'Female', 'HARRINGTON': 'Female', 'ISSA': 'Female', "J'VINI": 'Female',
        'NDOYE': 'Female', 'NILSSON': 'Female', 'RENO': 'Female', 'ZORA': 'Female', 
        'GABRIELLE' : 'Female',
    }

    approximations = {
        'TAMETS': 'STAMETS',
        'SETMER': 'DETMER',
        "T'RNA": "T'RINA",
        'OWOSEKAN': 'OWOSEKUN',
        'OWOSEKUM': 'OWOSEKUN',
        'ADORA': 'ADIRA',
        'ADRIA': 'ADIRA',
        'BRUCE': 'BRYCE',
        'BURHNAM': 'BURNHAM',
        'CHRISTOPER': 'CHRISTOPHER',
        'CHRSTOPHER': 'CHRISTOPHER',
        'COOMPUTER': 'COMPUTER',
        'CORTZ': 'CORTEZ',
        'FEFLIX': 'FELIX',
        'FELX': 'FELIX',
        'GABRIELLE': 'LORCA',
        "J'VINNI": "J'VINI",
        'NILLSON': 'NILSSON'
    }
    transcript_files = glob.glob('DSC*.txt')
    word_count = Counter()

    for file_path in transcript_files:
        _, filename = os.path.split(file_path)
        season, episode, _ = re.match(r'DSC(\d{2})(\d{2})-(.*)\.txt', filename).groups()

        words = collect_bechdel_passing_words(file_path, gender_dict)
        word_count.update(words)

    # Sort words by frequency
    sorted_words = [{'Word': word, 'Count': count} for word, count in word_count.most_common()]

    df = pd.DataFrame(sorted_words)
    return df

if __name__ == "__main__":
    word_df = main()
    print(word_df)

    # Save to CSV file
    csv_file_path = 'bechdel_passing_words_sorted.csv'
    word_df.to_csv(csv_file_path, index=False)
    print(f"Word data saved to {csv_file_path}")





