import subprocess
import re
import sys

try:
    filename = sys.argv[1]
except:
    print("Usage: python3 {} filename.mid".format(sys.argv[0]))
    exit(1)

try:
    import py_midicsv as pm
except:
    package = 'py_midicsv'
    #Use pip to install the package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    import py_midicsv as pm

midi_note_dict = {
0:'rest',
21:'A0',22:'A#0',23:'B0',
24:'C1',25:'C#1',26:'D1',27:'D#1',28:'E1',29:'F1',30:'F#1',31:'G1',32:'G#1',33:'A1',34:'A#1',35:'B1',
36:'C2',37:'C#2',38:'D2',39:'D#2',40:'E2',41:'F2',42:'F#2',43:'G2',44:'G#2',45:'A2',46:'A#2',47:'B2',
48:'C3',49:'C#3',50:'D3',51:'D#3',52:'E3',53:'F3',54:'F#3',55:'G3',56:'G#3',57:'A3',58:'A#3',59:'B3',
60:'C4',61:'C#4',62:'D4',63:'D#4',64:'E4',65:'F4',66:'F#4',67:'G4',68:'G#4',69:'A4',70:'A#4',71:'B4',
72:'C5',73:'C#5',74:'D5',75:'D#5',76:'E5',77:'F5',78:'F#5',79:'G5',80:'G#5',81:'A5',82:'A#5',83:'B5',
84:'C6',85:'C#6',86:'D6',87:'D#6',88:'E6',89:'F6',90:'F#6',91:'G6',92:'G#6',93:'A6',94:'A#6',95:'B6',
96:'C7',97:'C#7',98:'D7',99:'D#7',100:'E7',101:'F7',102:'F#7',103:'G7',104:'G#7',105:'A7',106:'A#7',107:'B7',
108:'C8'
}


#Parse the midi file into a csv text format
csv_string = pm.midi_to_csv(filename)

#Extract the clocks per quarter note from the header
regex = re.compile("\d+, \d+, .+, \d+, \d+, (\d+)")
clocks_per_quarter = int(regex.match(csv_string[0]).group(1))

#Remove all the lines before the note data
print("Removing unneccesary lines.")
while "Note_on_c" not in csv_string[0]:
    csv_string.pop(0)

#Remove all lines after note data
while "Note_off_c" not in csv_string[-1]:
    csv_string.pop()

#Remove extraneous information from remaining lines

#Regex for parsing out the time and note from each line
regex = re.compile("\d+, (\d+), .+, \d+, (\d+), \d+")

cleaned_lines = []
print("Parsing note lines.")
for line in csv_string:
    regex_result = regex.match(line)
    #Extract the time and note using the regex
    time_note = regex_result.group(1, 2)

    #Convert them to integers
    time_note = tuple([int(a) for a in time_note])

    cleaned_lines.append(time_note)

#Now, determine the length and kind of each note
notes = []

current_note = None
print("Cleaning lines.")
for time_note in cleaned_lines:
    if current_note:
        #If a note is currently pressed
        duration = time_note[0] - current_note[0]
        note = midi_note_dict[time_note[1]]

        notes.append((note, duration))
        current_note = None
    else:
        current_note = time_note

#Now notes is in the format (A4, 256), (C5, 512) for example

#Now we just need to convert from clocks to note type
note_length_dict = {
clocks_per_quarter / 16: 'sixtyfourthNote',
clocks_per_quarter / 8 : 'thirtysecondNote',
clocks_per_quarter / 4 : 'sixteenthNote',
clocks_per_quarter / 2 : 'eigthNote',
clocks_per_quarter     : 'quarterNote',
clocks_per_quarter * 2 : 'halfNote',
clocks_per_quarter * 4 : 'wholeNote',
clocks_per_quarter * 8 : 'doublewholeNote',
clocks_per_quarter * 16: 'quadruplewholeNote'
}

#Change the second entry to the corresponding dictionary value
notes = [(note[0], note_length_dict[note[1]]) for note in notes]

print("Writing to file...")
with open("plain_{}.txt".format(filename), 'w') as f:
    #[1:-1] to avoid the brackets of the list
    note_string = str(notes)[1:-1]
    note_string = note_string.replace("'", "")
    f.write(note_string)
print("Successfully saved the converted file to {}".format("plain_{}.txt".format(filename)))
