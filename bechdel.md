# Running the Bechdel test in Python
## dsc-bechdel-test.py

View [Python file](https://github.com/kelknightly/DSC/blob/main/dsc-bechdel-test.py)
View [Tableau visualization](https://public.tableau.com/app/profile/kelly.quantrill/viz/TheWomenofStarTrekDiscovery/Dashboard1)

The Bechdel test is a way of measuring of the representation of women in film and other fiction. The test asks whether a work features at least two named female characters who have a conversation about something other than a man.

This mini-project evaluates whether season 1 and season 4 of Star Trek Discovery pass the Bechdel test. Season 2 and 3 are not included at this time because episode transcripts are not yet available. All transcripts are sourced from [chakoteya.net](http://www.chakoteya.net/STDisco17/episodes.html).

Research inspired by the work of Jarrah Hodge who has evaluated classic Trek in similar ways:
- The Mary Sue - [How Does Your Favorite Star Trek Series Fare on the Bechdel Test?](https://www.themarysue.com/star-trek-bechdel-test/)
- Trekkie Feminist - [Star Trek: The Original Series Bechdel-Wallace Test Results](https://trekkiefeminist.com/star-trek-the-original-series-bechdel-wallace-test-results/)

Notably, Star Trek Discovery episode 1 season 1, 'The Vulcan Hello', which aired in September 2017, passes the Bechdel test with the very first character interction we see. 

> BURNHAM: We come in peace. That's why we're here. Isn't that the whole idea of Starfleet?
>
> GEORGIOU: Hey, I taught you that.
>
> BURNHAM: You don't trust me, Captain?
>
> GEORGIOU: I trust you with my life, Commander Burnham, but it doesn't change the fact that you're lost. Very lost.
>
> BURNHAM: Technically, we would be lost.
>
> GEORGIOU: How long until that storm comes crashing down on us?
>
> BURNHAM: I estimate one hour, 17 minutes, 22 seconds. Which is why I've made sure we're not lost. The map says the well is this way, Captain.
>
> (They walk on.)
>
> BURNHAM: This drought's going to last 89 years. The Crepusculans are facing extinction as a species. See those egg sacs? Those are their offspring.
>
> GEORGIOU: They've survived here for over a thousand years, Michael.
>
> BURNHAM: Right, and if we don't do something now, they won't live another thousand hours. The ambient radiation from a nearby drilling accident dried out their water table. If we can get in and out without making contact, we can steer clear of General Order One. And there is the well.
>
> GEORGIOU: I stand corrected.
>
> BURNHAM: Ye of little faith.
>
> GEORGIOU: Oh, never had a doubt. (powers up phaser rifle) Tell me what I need to break through this bedrock.
>
> BURNHAM: Point 7 second field burst at level setting 13.5.
>
> (Three shots are sent down the well. Rumble, then water erupts out.)
>
> GEORGIOU: Georgiou to Shenzhou. Two to transport.

This piece of sample dialogue proved very useful when iterating through the process of designing the script because I was able to use it to refine my analytical process and avoid false negatives. 

## Step 1: Preparing the TXT files
I manually visited each episode transcript on [chakoteya.net](http://www.chakoteya.net/STDisco17/episodes.html) and copy/pasted the contents into individual TXT files using Notepad. This allowed me to visually inspect each file for extraneous contents that might trip up my script later on, such as the header, footer, and embedded advertisements, and remove them. This can be done programmatically but since there were only 28 episode transcripts available and I had already started the visual inspection of each one, it seemed quicker to just conduct this manually. 

Each TXT file was saved with the following naming convention: 
- DSC[episodenumber][seasonnumber]-[episode-title]

For example: 
- DSC0101-the-vulcan-hello.txt
- DSC0102-battle-at-the-binary-stars.txt
- DSC0102-context-is-for-kings.txt
- DSC0104-the-butchers-knife-cares-not-for-the-lambs-cry.txt
- DSC0105-choosse-your-pain.txt

Be sure to save these in the project folder on your computer where you'll be running your Python script from. All files should be in the same location for ease of use. 

## Step 2: Importing Python libraries

View the full Python script [here](https://github.com/kelknightly/DSC/blob/main/dsc-bechdel-test.py).

The first thing we want to do is import the Python libraries we intend to use in our script. 

```
import re
import os
import glob
import pandas as pd
```

The 're' library stands for Regular Expression in Python, also referred to as [RegEx](https://www3.ntu.edu.sg/home/ehchua/programming/howto/Regexe.html). The 're' library is widely used in Pythn for string search and manipulation. It's essential for pattern matching, parsing, and complex text processing tasks.
In the Bechdel script, RegEx is used to process and analyze text data. Specifically, it helps to identify dialogue lines from the TXT files using patterns to match character names and their spoken lines and to search for mentions of male-specific words or names within those lines. 

The os (Operating System) library is used for interacting with the operating system. provides a way of using operating system-dependent functionality like reading or writing to the filesystem, navigating directories, managing paths, and accessing environment variables. In the context of the Bechdel script, it is used for path manipulations or to handle file operations, such as opening files in different directories.

The glob library is used for file handling, specifically to find all the pathnames matching a specified pattern (like 'DSC*.txt'), which is helpful in the script to automatically find and process all transcript files. glob is commonly used to retrieve files/pathnames matching a particular pattern (using Unix shell rules instead of regular expressions). It's handy for reading multiple files of a specific type from a directory.

pandas is a data manipulation and analysis library. In the Bechdel script, it's used to create, manipulate, and export data structures like DataFrames, which store the results of the analysis and prepare them for output (e.g., writing to a CSV file).
pandas is a powerful tool in Python for data analysis and manipulation. It's widely used in data science for cleaning, transforming, analyzing, and visualizing data. Its primary data structure, the DataFrame, is especially useful for handling structured data.

These libraries collectively support text processing (through re), file and directory management (using os and glob), and data analysis and export (with pandas). They are essential in Python for handling a wide range of tasks involving data processing, file management, and pattern matching.

## Step 3: Defining the key Bechdel test function that analyzes each episode

The analyze_episode function is a key component of the Python script designed to analyze TV show or movie transcripts for the Bechdel test and additional metrics related to female dialogue. Let's break down what each part of the function does:

```
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
```

1. Function Definition:
    - def analyze_episode(file_path, gender_dict):
    - This line defines the function analyze_episode, which takes two arguments: file_path, the path to a transcript file, and gender_dict, a dictionary mapping character names to their gender.
2. Regular Expression Compilation:
    - dialogue_pattern = re.compile(r'^([A-Z][A-Z\s\']*):\s*(.*)')
    - Here, a regular expression pattern is compiled to identify dialogue lines in the transcript. It matches lines where a character's name (in all caps) is followed by a colon and then their spoken dialogue.
3. Initializing Variables:
    - Several variables are initialized to store information:
        - female_characters_in_conversation: A set to keep track of female characters involved in Bechdel-passing dialogues.
        - female_words: A counter for the number of words spoken by female characters.
        - total_words: A counter for the total number of words in the episode.
        - prev_character and prev_dialogue: Variables to remember the previous character and their dialogue (for context in conversations).
        - bechdel_pass: A boolean flag to indicate whether the episode passes the Bechdel test.
4. File Processing Loop:
    - The with open(file_path, 'r') as file: block opens the transcript file for reading.
    - for line in file: iterates over each line in the file.
5. Dialogue Line Processing:
    - match = dialogue_pattern.match(line)
    - This line checks if the current line in the file matches the dialogue pattern (character name followed by dialogue).
    - If a match is found, character, dialogue = match.groups() extracts the character name and their spoken words.
6. Word Counting and Gender Check:
    - The script counts the words in each line of dialogue and updates total_words.
    - If the character is female (as per gender_dict), their words are added to female_words.
    - The script then checks if the dialogue is part of a conversation between two different female characters, and whether the conversation is about men (using the regex search for male pronouns or terms). If not, it's considered as contributing to the Bechdel test pass.
7. Calculate Female Speaking Percentage:
    - female_speaking_percentage = (female_words / total_words) * 100
    - This line calculates the percentage of the episode's dialogue that is made up of words spoken by female characters.
8. Return Statement:
    - The function returns three values:
        - bechdel_pass: Whether the episode passes the Bechdel test.
        - A string of female characters involved in Bechdel-passing conversations.
        - female_speaking_percentage: The percentage of dialogue in the episode spoken by female characters.

'analyze_episode' processes a script file to determine if it passes the Bechdel test, identifies which female characters contribute to this, and calculates what percentage of the dialogue is spoken by female characters. This function is crucial for analyzing scripts for gender representation and dialogue balance.

## Step 4: Gender dictionary and approximations
The main() function in our script serves as the central execution point for analyzing the episode transcripts according to the Bechdel test and other criteria. It sets up essential data structures and orchestrates the overall process by setting up key variables and structures that are needed before the script begins processing the individual transcript files. It prepares the ground for a detailed analysis based on the predefined criteria (gender of characters, approximations for names, and the files to be analyzed). The results of this analysis are intended to be compiled into the results list, which can then be further processed or outputted as needed.

```
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
```

1. gender_dict:
This dictionary maps character names to their identified gender. In the Bechdel test context, this is crucial for identifying which characters are female. For example, 'BURNHAM': 'Female' indicates that the character named BURNHAM is female. This dictionary is used throughout the script to determine whether dialogues involve female characters, which is a key part of the Bechdel test.

2. approximations:
This dictionary is used for correcting common typos or alternate spellings in character names within the scripts. For example, 'TAMETS': 'STAMETS' suggests that any occurrence of TAMETS in the script should be considered as STAMETS. This is important for accurately identifying characters, especially in cases where scripts might have inconsistencies in spelling.
3. Finding Transcript Files:
transcript_files = glob.glob('DSC*.txt')
This line uses the glob library to find all files in the current directory that match the pattern 'DSC*.txt'. These are the script files for the different episodes. The pattern 'DSC*.txt' is designed to match filenames that start with 'DSC' and end with '.txt', which is a common naming convention for text files.
4. Initializing results:
results = []
This initializes an empty list named results, which will later be used to store the outcomes of the analysis (like whether each episode passes the Bechdel test, the speaking percentage of female characters, etc.).

## Step 5: The 'for' loop within the 'main' function
The for loop within the main function of the script is designed to iterate over each transcript file, analyze it, and collect relevant data about female character participation and the Bechdel test compliance. It systematically processes each transcript file, extracts and formats necessary information, applies the Bechdel test analysis, and compiles all results into a structured DataFrame for further use.

```
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
```

1. Iterating Over Transcript Files:
    - for file_path in transcript_files:
    - This line starts a loop that iterates through each file path stored in the transcript_files list, which contains the paths to all the transcript files matching the 'DSC*.txt' pattern.
2. Extracting Episode Information:
    - _, filename = os.path.split(file_path)
    - season, episode, title = re.match(r'DSC(\d{2})(\d{2})-(.*)\.txt', filename).groups()
    - These lines extract information from the file path. The os.path.split function separates the file path into the directory and the filename. The regular expression re.match then extracts the season number, episode number, and title from the filename. The pattern r'DSC(\d{2})(\d{2})-(.*)\.txt' is designed to parse filenames formatted like 'DSC0101-some-title.txt', capturing the season and episode numbers and the title.
3. Formatting the Episode Title:
    - formatted_title = ' '.join(word.capitalize() for word in title.split('-'))
    - This line formats the episode title for readability. It splits the title on hyphens, capitalizes each word, and then joins them back together with spaces.
4. Analyzing the Episode:
    - bechdel_test_pass, contributing_characters, female_speaking_percentage = analyze_episode(file_path, gender_dict)
    - The analyze_episode function is called with the current file path and the gender dictionary. It returns whether the episode passes the Bechdel test, the names of contributing female characters, and the percentage of dialogue spoken by female characters.
5. Storing the Results:
    - results.append({...})
    - This line appends a dictionary to the results list. The dictionary contains the season, episode, formatted title, Bechdel test result, contributing female characters, and female speaking percentage. This is essentially compiling the analysis results for each episode.
6. Creating a DataFrame from Results:
    - df = pd.DataFrame(results)
    - After the loop has processed all files, the results list is converted into a pandas DataFrame. This DataFrame is a structured way to store the data, making it easy to export, analyze further, or visualize.
7. Returning the DataFrame:
    - return df
    - Finally, the DataFrame df is returned from the main function. This DataFrame contains all the processed data from the script's analysis.

## Step 6: Executing
The final piece of the script is where the actual execution of the program occurs. Results are displayed and the data is saved for external use, making it a critical segment for both verification and practical application of the script's functionality.

```
if __name__ == "__main__":
    analysis_df = main()
    print(analysis_df)

    # Save to CSV file
    csv_file_path = 'star_trek_discovery_analysis.csv'
    analysis_df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")
```

1. if __name__ == "__main__"::
This is a common Python idiom for conditionally executing code. The __name__ variable in Python is a special built-in variable that gets assigned a string depending on how the containing script is being used.
When the script is run as a standalone program (i.e., not imported as a module in another script), __name__ is set to "__main__". Therefore, the code inside this 'if' block will only execute if the script is run directly, and not if it's imported into another script.

2. Calling the main Function and Storing the Result:
analysis_df = main()
This line calls the main() function defined earlier in the script. The main() function processes the transcript files and returns a pandas DataFrame (analysis_df) containing the analysis results (Bechdel test pass/fail, contributing characters, and speaking percentages).

3. Printing the DataFrame:
print(analysis_df)
This line prints the DataFrame to the console. It's a way to visually inspect the results of the script immediately after it finishes running.

4. Saving the DataFrame to a CSV File:
The lines below are responsible for exporting the DataFrame to a CSV file. 
csv_file_path is a string variable holding the name of the CSV file where the results will be saved.
analysis_df.to_csv(csv_file_path, index=False) uses the to_csv method of the DataFrame to write its content to a CSV file. The index=False parameter is used to tell pandas not to write row indices into the CSV file.

```
csv_file_path = 'star_trek_discovery_analysis.csv'
    analysis_df.to_csv(csv_file_path, index=False)
```

5. Confirming Data Save:
print(f"Data saved to {csv_file_path}")
This line prints a confirmation message to the console, indicating that the data has been successfully saved to the specified CSV file.

