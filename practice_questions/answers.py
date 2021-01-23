"""
Practice solving random problems
"""


import click
import numpy as np


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    pass


@cli.command('first_letter', help='Write a function that takes in a '\
                             'string and counts the number of occurrences of each '\
                             'first letter of each word.  Output "a=1, b=2, etc."')
@click.option('-s', '--in_str', help='Input string')
def first_letter(in_str):
    """
    Write a function that takes in a string and counts the number of occurrences of each 
    first letter of each word.  Output "a=1, b=2, etc."
    """
    if type(in_str) is not str:
        raise TypeError('input arg in_str {} is not of type str'.format(in_str))
    
    # get the individual words from the input string
    pieces = in_str.split(' ')
    print('PIECES: {}'.format(pieces))

    # get the first letter as lowercase from each word
    first_letters = [word[0].lower() for word in pieces]

    # initialize an empty dict that will store counts for each letter
    results = dict()

    for letter in first_letters:
        if not results.get(letter):
            results[letter] = 1
        else:
            results[letter] += 1

    # initialize an empty list that will store our output strings
    output = []

    for letter, count in results.items():
        output.append('{}={}'.format(letter, count))

    # format the final output string
    result = ', '.join(output)
    print('RESULT: {}'.format(result))

    return result


@cli.command('phone_number', help='Generate a list of phone numbers using a length of the numbers '\
                             'and a list of disallowed digits. The numbers cannot have 2 identical '\
                             'digits in a row (e.g. 2235) and if a number has a "4" in it, then '\
                             'the number must begin with a 4')
@click.option('-l', '--length', type=int, help='Length of phone numbers (i.e. number of digits)')
@click.option('-d', '--disallowed', type=int, multiple=True, help='Disallowed digits')
def phone_number(length, disallowed):
    # determine what the 'max' phone number digits will be
    # e.g. if length is 5, the max number would be '99999'
    max_number = int('9' * length)
    # print(max_number)

    # generator of all possible numbers from 1 up to the max number
    # use the string method zfill to add appropriate number of leading zeros
    initial_numbers = (str(n).zfill(length) for n in range(1, max_number + 1))
    # print(initial_numbers[:10])

    # we need to enforce that if a '4' is in the number, than the number
    # must begin with a '4'.  Create a new list to store the results.
    def handle_fours(num):
        if '4' in num:
            n = '4' + num[1:]
        else:
            n = num
        return n

    intermediate_numbers = (handle_fours(q) for q in initial_numbers)

    # Next, we need to enforce the rule that a phone number cannot have 2 of the 
    # same digits in a row.
    def filter_simultaneous(num: int):
        valid = True
        for ind in range(1, length):
            if num[ind-1] == num[ind]:
                valid = False
                break
        return valid

    itermediate_numbers_ = filter(filter_simultaneous, intermediate_numbers)

    # finally, remove any numbers with a disallowed digit
    def filter_disallowed(num):
        valid = True
        for d in disallowed:
            if str(d) in num:
                valid = False
                break
        return valid

    final_numbers = filter(filter_disallowed, itermediate_numbers_)

    # conversion to a set removes duplicates, the final object is a sorted list
    final_result = sorted(list(set((final_numbers))))

    print('LENGTH FINAL NUMBERS: {}'.format(len(final_result)))
    print('FINAL NUMBERS: {}'.format(final_result[-10:]))
    
    return final_result


@cli.command('broken_key', help='A typewriter has a broken key - this function ' \
                                'takes an input number and a broken key, then ' \
                                'outputs the next highest possible number to the ' \
                                'input number that can be written by the typewriter. \n' \
                                'e.g. broken_key(12345, 2) --> 11999')
@click.option('-i', '--input-number', type=int, help='The input number')
@click.option('-b', '--broken', type=int, help='Number between 0-9 representing the broken key')
def broken_key(input_number, broken):
    # convert the number to a string, should make it easier to test each digit
    num = str(input_number)
    
    # get the individual digits by converting the string to a list
    digits = list(num)  # e.g. '1234' --> ['1', '2', '3', '4']
    number_digits = len(num)
    
    for n in range(0, number_digits):
        if digits[n] == str(broken):
            # update the broken digit to be the next highest number
            digits[n] = str(max(0, int(digits[n]) - 1))
            break
    
    # these are the digits that we have to adjust (right of the changed number)
    update_digits = range(n+1, number_digits) if n+1 < number_digits else []

    for x in update_digits:
        digits[x] = '9'

    output = int(''.join(digits))
    print('HIGHEST POSSIBLE NUMBER: {}'.format(output))

    return output

@cli.command('array_match', help='Count how many iterations it takes to match random numbers ' \
                                 'with a randomly generated array of shape (100,100). ' \
                                 'The counter will report the number of iterations once any of ' \
                                 'the following are completed: row, column, diagonal.  ' \
                                 'All numbers are in the inclusive range of 1 and 1e6.')
@click.option('-a', '--array', default=None)
def array_match(array):
    def check_complete(in_array):
        vals = [z for z in in_array if z != 0]
        if len(vals) == 100:
            return True
        else:
            return False

    if not array:
        array = np.random.randint(1, 1e6, (100, 100))

    collect = np.zeros((100, 100), dtype=np.int8)

    match = False
    counter = 0

    while not match:
        counter += 1
        n = np.random.randint(1, 1e6)
        if n in array:
           x, y = np.where(array==n)

           x = x[0]
           y = y[0]

           collect[(x, y)] = 1

           col = collect[:,y]
           row = collect[x,:]
           diag1 = np.diagonal(collect)
           diag2 = np.diagonal(collect, axis1=1, axis2=0)

           if any(list(map(check_complete, [col, row, diag1, diag2]))):
               match = True

    print('Number of iterations: {}'.format(counter))

    return counter


if __name__ == '__main__':
    cli()
