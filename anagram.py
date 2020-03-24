import random


def anagram(value):
    '''Returns random anagram of given value'''
    return ''.join(random.sample(value, len(value)))

