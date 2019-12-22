# midi_to_plain_text
A python program to convert extremely simple midi files into plain text.

Takes in a simple midi file consisting of only single notes and rest, and saves a new file with tuples of note type and duration.

For example, a midi file containing the A major scale as included in the file example_scale.mid would save

(A3, wholeNote), (B3, wholeNote), (C#4, wholeNote), (D4, wholeNote), (E4, wholeNote), (F#4, wholeNote), (G#4, wholeNote), (A4, wholeNote)

to the file plain_example_scale.mid.txt
