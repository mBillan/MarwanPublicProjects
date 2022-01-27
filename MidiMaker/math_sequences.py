"""
Create musicals based on the popular math sequences like: Fibonacci, Prime numbers,

Note: Make sure that you imported the package "mido"
"""

from midi_utils import get_notes_range
from mido import Message, MidiFile, MidiTrack


def first_n_fibonaccis(nth_element):
    fib_array = [0, 1]

    def fibonacci(n):
        # Check is n is less than 0
        if n <= 0:
            print("Incorrect input")

        # Check is n is less than len(FibArray)
        elif n <= len(fib_array):
            return fib_array[n - 1]
        else:
            temp_fib = fibonacci(n - 1) + fibonacci(n - 2)
            fib_array.append(temp_fib)
            return temp_fib

    fibonacci(nth_element)

    return fib_array


def numeric_list_to_digits(numeric_list):
    """
    Convert a list of numbers to a list of digits.
    Each number is converted to its digits.
    :param numeric_list: A list of numbers
    :return: A new list containing the of the original numbers according to the same order.
    """
    digits_list = []
    for num in numeric_list:
        # Number to a list of it's digits
        digits = [int(digit) for digit in list(str(num))]
        digits_list = digits_list + digits

    return digits_list


def fibonacci_in_midi(output_midi="musical_fibo_line.mid"):
    """
    Generate a midi musical based on the Fibonacci sequence.
    Each number in the sequence is converted to its digits and each digit is played separately.
    Thus, creating a Fibonacci melody.

    :param output_midi: The name of the file to save the midi output file in.
    :return: none
    """
    # TODO: Take the midi building block to the utils file and make it more generic.
    outfile = MidiFile()

    track = MidiTrack()
    outfile.tracks.append(track)
    track.append(Message('program_change', program=12))

    delta_ticks = 120
    notes_range = get_notes_range()

    # Get the first 24 Fibonacci numbers
    fibo_nums = first_n_fibonaccis(24)
    # Convert them into a list of digits
    fibo_digits = numeric_list_to_digits(fibo_nums)

    for col in range(len(fibo_digits)):
        # Each Fibo digit is a single note played alone.
        # TODO: Add relevant chords at the beginning of each bar
        notes_to_hit = [notes_range[fibo_digits[col]]]

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
    fibonacci_in_midi()

