"""
Create musicals based on the popular math sequences like: Fibonacci, Prime numbers,

Note: Make sure that you imported the package "mido"
"""

from midi_utils import sequence_to_midi, Chord


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
        digits = [Chord([int(digit)]) for digit in list(str(num))]
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
    # Get the first 24 Fibonacci numbers
    fibo_nums = first_n_fibonaccis(24)
    print(f"Got these Fibonacci elements:{fibo_nums}")

    # Convert them into a list of digits
    fibo_digits = numeric_list_to_digits(fibo_nums)
    print(f"Transform it to a list of chords:{fibo_digits}")

    # TODO: Add relevant chords at the beginning of each bar

    print("Convert it to midi file")
    sequence_to_midi(chords_sequence=fibo_digits, output_midi=output_midi)
    

def pi_digits_midi(output_midi="pi_digits.mid"):
    """
    Generate a midi musical based on the PI number.
    Each digit in the number (3.14...) is converted to a note and each note is played separately.
    Thus, creating a PI melody.

    :param output_midi: The name of the file to save the midi output file in.
    :return: none
    """
    pi = 22/7
    pi_list = list(f"{pi:.52f}")
    pi_list.remove('.')
    print(f"Here are the pi digits: {pi_list}")
    pi_chords = [Chord([int(digit)]) for digit in pi_list]
    sequence_to_midi(chords_sequence=pi_chords, output_midi=output_midi)


if __name__ == "__main__":
    fibonacci_in_midi()
    # pi_digits_midi()
