import re
import os
import glob
import pandas as pd

def analyze_episode(file_path, gender_dict):
    dialogue_pattern = re.compile(r'^([A-Z][A-Z\s\']*):\s*(.*)')

    female_characters_in_conversation = set()
    female_words = 0
    total_words = 0
    prev_character = None
    prev_dialogue = ""
    bechdel_pass = False

    with open(file_path, 'r') as file:
        for line in file:
            match = dialogue_pattern.match(line)
            if match:
                character, dialogue = match.groups()
                character = character.strip().upper()

                word_count = len(dialogue.split())
                total_words += word_count

                if gender_dict.get(character) == 'Female':
                    female_words += word_count
                    if prev_character and prev_character != character:
                        combined_dialogue = prev_dialogue + " " + dialogue
                        if not re.search(r'\b(he|him|his|man|men|guy|guys|boy|boys)\b', combined_dialogue, re.IGNORECASE):
                            female_characters_in_conversation.update([prev_character, character])
                            bechdel_pass = True
                    prev_character = character
                    prev_dialogue = dialogue

    female_speaking_percentage = (female_words / total_words) * 100 if total_words > 0 else 0

    return bechdel_pass, ', '.join(female_characters_in_conversation), female_speaking_percentage

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
    results = []

    for file_path in transcript_files:
        _, filename = os.path.split(file_path)
        season, episode, title = re.match(r'DSC(\d{2})(\d{2})-(.*)\.txt', filename).groups()
        formatted_title = ' '.join(word.capitalize() for word in title.split('-'))

        bechdel_test_pass, contributing_characters, female_speaking_percentage = analyze_episode(file_path, gender_dict)

        results.append({
            'Season': int(season),
            'Episode': int(episode),
            'Title': formatted_title,
            'Bechdel Test': 'Pass' if bechdel_test_pass else 'Fail',
            'Contributing Female Characters': contributing_characters,
            'Female Speaking Percentage': female_speaking_percentage
        })

    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":
    analysis_df = main()
    print(analysis_df)

    # Save to CSV file
    csv_file_path = 'star_trek_discovery_analysis.csv'
    analysis_df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")






    