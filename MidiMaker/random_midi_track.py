#!/usr/bin/env python
"""
Create a new MIDI file with some random notes.

Note: Make sure that you imported the package "mido"
"""
from __future__ import division
import random
from mido import Message, MidiFile, MidiTrack  #, MAX_PITCHWHEEL, bpm2tempo, tick2second
from midi_utils import get_notes_range


def generate_random_midi(number_of_beats=32, output_midi="musical_line.mid"):
    """
    Generates a random musical line (in midi format) with an exact number of beats with the same basic rythem.

    :param number_of_beats: The number of the beats (or chords) to generate.
    :param output_midi: The name of the file to save the midi output file in.
    :return: None
    """
    outfile = MidiFile()

    track = MidiTrack()
    outfile.tracks.append(track)

    track.append(Message('program_change', program=12))

    # track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(80)))

    delta_ticks = 120

    notes_range = get_notes_range()

    # Choose the notes to play for each beat
    for idx in range(number_of_beats):
        # Each beat can have between 1-4 notes played as a chord
        num_of_notes = random.choices(range(1, 4))[0]
        notes_to_hit = random.choices(notes_range, k=num_of_notes)

        # Hit the notes
        for note in notes_to_hit:
            track.append(Message('note_on', note=note, velocity=100, time=0))

        # Configure the pitch of the activated notes
        track.append(Message('pitchwheel', pitch=60, time=delta_ticks * 2))

        # Release the note
        for note in notes_to_hit:
            track.append(Message('note_off', note=note, velocity=100, time=0))

    outfile.save(output_midi)


if __name__ == "__main__":
    generate_random_midi()

