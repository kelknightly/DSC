import re
import glob

def find_approximations(files):
    dialogue_pattern = re.compile(r'^([A-Z][A-Z\s\']*):\s*(.*)')
    character_counts = {}

    for file_path in files:
        with open(file_path, 'r') as file:
            for line in file:
                match = dialogue_pattern.match(line)
                if match:
                    character, _ = match.groups()
                    character = character.strip().upper()
                    character_counts[character] = character_counts.get(character, 0) + 1

    # Identifying potential approximations based on similarity and frequency
    approximations = {}
    for char in character_counts:
        for other_char in character_counts:
            if char != other_char and len(char) > 3 and len(other_char) > 3:
                if char.startswith(other_char[:3]) or other_char.startswith(char[:3]):
                    if character_counts[char] < character_counts[other_char]:
                        approximations[char] = other_char

    return approximations

# List of transcript files
transcript_files = glob.glob('path_to_your_transcript_files/DSC*.txt')

# Finding character name approximations
character_approximations = find_approximations(transcript_files)
print(character_approximations)
