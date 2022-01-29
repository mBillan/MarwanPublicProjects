"""
Convert a text to a midi musical file that looks like the Ascii Art of that text
Note: Make sure that you imported the package "mido"
"""
from midi_utils import sequence_to_midi, Chord
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


def characters_to_chords(rows_of_characters):
    """
    Convert an ascii art list to chords

    :param rows_of_characters: The ascii art represented as a list of lists of characters in ['', '#']
    :return: List chords based on the given ascii art
    """
    chords = []
    for col in range(len(rows_of_characters[0])):
        # Convert each '#' into the number of the row it's in
        curr_chord = Chord([len(rows_of_characters) - row for row in range(len(rows_of_characters))
                            if rows_of_characters[row][col] == '#'])
        chords = chords + [curr_chord]

    return chords


def text_to_midi(text="hello world", output_midi="musical_ascii_line.mid"):
    """
    Convert a text to a midi musical file that looks like the Ascii Art of that text

    :param text: The text to convert
    :param output_midi: The name of the file to save the midi output file in.
    :return: None
    """
    ascii_art_list = text_to_ascii_art(text)
    chords = characters_to_chords(ascii_art_list)
    for chord in chords:
        print(chord.notes)
    sequence_to_midi(chords, output_midi=output_midi)


if __name__ == "__main__":
    text_to_midi(text="hello world")
