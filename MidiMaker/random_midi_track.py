"""
Create a new MIDI file with some random notes.

Note: Make sure that you imported the package "mido"
"""
from __future__ import division
import random
from midi_utils import sequence_to_midi


def get_random_chords(num_of_chords):
    """
    Generates random chords.

    :param num_of_chords: The number of the chords
    :return: A list of the generated chords
    """
    chords = []
    for idx in range(num_of_chords):
        # Each chord can have between 1-4 notes
        num_of_notes = random.choices(range(1, 4))[0]

        # Allow only 24 notes to be randomized
        notes_range = range(24)

        # Randomize from the allowed notes
        curr_chords = random.choices(notes_range, k=num_of_notes)
        chords = chords + [curr_chords]

    return chords


def generate_random_midi(number_of_beats=32, output_midi="random_musical_line.mid"):
    """
    Generates a random musical line (in midi format) with an exact number of beats with the same basic rythem.

    :param number_of_beats: The number of the beats (or chords) to generate.
    :param output_midi: The name of the file to save the midi output file in.
    :return: None
    """
    random_chords = get_random_chords(num_of_chords=number_of_beats)
    print(random_chords)
    sequence_to_midi(sequence=random_chords, output_midi=output_midi)


if __name__ == "__main__":
    generate_random_midi()

