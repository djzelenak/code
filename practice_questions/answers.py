"""
Now and then I come across programming questions - here is a rough attempt to collect some questions-answers
"""


import click


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


if __name__ == '__main__':
    cli()
