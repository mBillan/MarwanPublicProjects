"""
Utility classes, enums and definitions from the musical world that help configure the midi files

"""
from enum import Enum
from mido import Message, MidiFile, MidiTrack


class Scale(Enum):
    """
    A representation of the musical scales.
    Each scale is represented as a list of intervals from the base note.
    """
    MAJOR = [0, 2, 4, 5, 7, 9, 11, 12]
    MINOR = [0, 2, 3, 5, 7, 8, 10, 12]


class Note(Enum):
    """
    A representation of the middle flat notes.
    """
    A = 57
    B = 59
    C = 60  # middle C or C4
    D = 62
    E = 64
    F = 65
    G = 67


class Chord:
    def __init__(self, notes=[]):
        if not all(isinstance(n, int) for n in notes):
            raise Exception("The notes should all be in their integer representation")

        self.notes = notes


def get_notes_range(key=Note.A.value, scale: Scale = Scale.MAJOR.value):
    """
    Gets a valid notes range based on the given key and scale

    :param key: The key of the wanted notes
    :param scale: The scale of the wanted notes
    :return: A list of all the allowed notes.
    """
    notes = [key - 24 + dist for dist in scale] + \
            [key - 12 + dist for dist in scale] + \
            [key + dist for dist in scale] + \
            [key + 12 + dist for dist in scale]
    notes = list(dict.fromkeys(notes))

    return notes


def sequence_to_midi(chords_sequence: [Chord], output_midi="sequence.mid", key=Note.A.value, scale: Scale = Scale.MAJOR.value):
    """
    Generate a midi musical piece according to the given sequence of notes.

    :param scale:
    :param key:
    :param chords_sequence: A list of chords to be played one after another.
        Example: [[1], [5], [2,6], [7,3,5], [0]]
    :param output_midi: The name of the file to save the midi output file in.
    :return: none
    """
    outfile = MidiFile()

    track = MidiTrack()
    outfile.tracks.append(track)
    track.append(Message('program_change', program=12))

    delta_ticks = 120
    notes_range = get_notes_range(key=key, scale=scale)

    for chord in range(len(chords_sequence)):
        # Put the chords sequence in the allowed notes_range
        notes_to_hit = [notes_range[note] for note in chords_sequence[chord].notes]

        # Hit the notes
        for note in notes_to_hit:
            track.append(Message('note_on', note=note, velocity=100, time=0))

        # Configure the pitch of the activated notes
        track.append(Message('pitchwheel', pitch=60, time=delta_ticks * 2))

        # Release the note
        for note in notes_to_hit:
            track.append(Message('note_off', note=note, velocity=100, time=0))

    outfile.save(output_midi)
