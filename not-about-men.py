import re
import os
import glob
import pandas as pd
from collections import Counter

def analyze_character_dialogues(file_path, gender_dict):
    dialogue_pattern = re.compile(r'^([A-Z][A-Z\s\']*):\s*(.*)')
    male_reference_pattern = re.compile(r'\b(he|him|his|man|men|guy|guys|boy|boys)\b', re.IGNORECASE)

    character_dialogues = {}
    word_frequencies = Counter()
    prev_character = None

    with open(file_path, 'r') as file:
        for line in file:
            match = dialogue_pattern.match(line)
            if match:
                character, dialogue = match.groups()
                character = character.strip().upper()

                if gender_dict.get(character) == 'Female':
                    words = re.findall(r'\w+', dialogue.lower())
                    word_frequencies.update(words)

                    if character not in character_dialogues:
                        character_dialogues[character] = {'positive_lines': 0, 'negative_lines': 0}

                    mentions_men = male_reference_pattern.search(dialogue) is not None
                    mentions_men |= any(word.upper() not in gender_dict for word in re.findall(r'\b[A-Z][A-Z]+\b', dialogue))
                    speaking_to_female = prev_character and gender_dict.get(prev_character) == 'Female'

                    if not mentions_men and speaking_to_female:
                        character_dialogues[character]['positive_lines'] += 1
                    else:
                        character_dialogues[character]['negative_lines'] += 1

                prev_character = character

    return character_dialogues, word_frequencies

def calculate_scores_and_word_freq(gender_dict, transcript_files):
    overall_character_scores = {}
    total_word_frequencies = Counter()

    for file_path in transcript_files:
        character_dialogues, word_frequencies = analyze_character_dialogues(file_path, gender_dict)
        total_word_frequencies.update(word_frequencies)

        for character, counts in character_dialogues.items():
            total_lines = counts['positive_lines'] + counts['negative_lines']
            if total_lines > 0:
                score = (counts['positive_lines'] / total_lines) * 100
                if character in overall_character_scores:
                    overall_character_scores[character]['total_lines'] += total_lines
                    overall_character_scores[character]['total_score'] += score
                    overall_character_scores[character]['count'] += 1
                else:
                    overall_character_scores[character] = {'total_lines': total_lines, 'total_score': score, 'count': 1}

    # Calculate average scores
    for character in overall_character_scores:
        overall_character_scores[character]['average_score'] = overall_character_scores[character]['total_score'] / overall_character_scores[character]['count']

    return overall_character_scores, total_word_frequencies

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
    
    character_scores, word_frequencies = calculate_scores_and_word_freq(gender_dict, transcript_files)

    # Convert character scores to DataFrame
    character_scores_df = pd.DataFrame.from_dict(character_scores, orient='index', columns=['average_score', 'total_lines'])
    
    # Convert word frequencies to DataFrame
    word_freq_df = pd.DataFrame(word_frequencies.items(), columns=['Word', 'Frequency'])

    return character_scores_df, word_freq_df

if __name__ == "__main__":
    character_scores_df, word_freq_df = main()

    # Save to CSV files
    character_scores_csv = 'character_scores.csv'
    character_scores_df.to_csv(character_scores_csv)
    print(f"Character scores saved to {character_scores_csv}")

    word_freq_csv = 'word_frequencies.csv'
    word_freq_df.to_csv(word_freq_csv)
    print(f"Word frequencies saved to {word_freq_csv}")
