"""
Utility classes, enums and definitions from the musical world that help configure the midi files

"""
from enum import Enum


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
