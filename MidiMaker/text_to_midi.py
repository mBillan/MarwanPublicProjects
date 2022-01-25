"""
Convert a text to a midi musical file that looks like the Ascii Art of that text
Note: Make sure that you imported the package "mido"
"""
from mido import Message, MidiFile, MidiTrack
from midi_utils import get_notes_range

from pyfiglet import figlet_format


def text_to_ascii_art(text):
    """
    Convert a text to Ascii Art.

    :param text: The string that needs conversion
    :return: A 2D list that contains rows of a special character ('#') and spaces.
        The special character '#' is a place-holder for the notes.

    Example:
        text = "Hello",  would be converted to:
        #    # ###### #      #       ####
        #    # #      #      #      #    #
        ###### #####  #      #      #    #
        #    # #      #      #      #    #
        #    # #      #      #      #    #
        #    # ###### ###### ######  ####

        The first row of the list would be:
        ['#', ' ', ' ', ' ', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ']

    """
    # Convert the given text to Ascii Art (font="banner" generates '#' characters)
    ascii_art = figlet_format(text.lower(), font='banner')

    # Convert the Ascii Art to a list of rows of characters and spaces and return it
    return [list(line) for line in ascii_art.split('\n') if line.strip()]


def text_to_midi(text="hello world", output_midi="musical_ascii_line.mid"):
    outfile = MidiFile()

    track = MidiTrack()
    outfile.tracks.append(track)
    track.append(Message('program_change', program=12))

    delta_ticks = 120
    ascii_art_list = text_to_ascii_art(text)

    notes_range = get_notes_range()

    for col in range(len(ascii_art_list[0])):
        # Iterate over the Ascii text columns wise and convert each column to a chord

        # Each special character ('#') represents a note. The row number is the interval from the base note
        notes_char = [row for row in range(len(ascii_art_list)) if ascii_art_list[row][col] == '#']
        notes_to_hit = [notes_range[len(notes_range) - note_char - 4] for note_char in notes_char]

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
    text_to_midi(text="hello world")

