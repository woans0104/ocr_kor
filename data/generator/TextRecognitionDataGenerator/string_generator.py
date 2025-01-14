import random as rnd
import re
import string
import requests

from bs4 import BeautifulSoup

def create_strings_from_file(filename, count):
    """
        Create all strings by reading lines in specified files
    """

    strings = []

    with open(filename, 'r', encoding="utf8") as f:
        lines = [l[0:200] for l in f.read().splitlines() if len(l) > 0]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            if len(lines) >= count - len(strings):
                strings.extend(lines[0:count - len(strings)])
            else:
                strings.extend(lines)

    return strings

def create_strings_from_dict(length, allow_variable, count, lang_dict):
    """
        Create all strings by picking X random word in the dictionnary
    """
    lang_dict = lang_dict[0]
    dict_len = len(lang_dict)
    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length) if allow_variable else length):
            current_string += lang_dict[rnd.randrange(dict_len)]
            current_string += ''
        strings.append(current_string)
    return strings

def create_strings_from_dict_v2(length, allow_variable, count, lang_dict):
    """
        Create all strings by picking X random word in the dictionnary
    """


    dict1,dict2 = lang_dict[0], lang_dict[1]

    dict1_len = len(dict1)
    dict2_len = len(dict2)

    strings = []

    check = 'no_1'

    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length+1) if allow_variable else length+1):
            if check == 'no_1':
                current_string += dict1[rnd.randrange(dict1_len)]
                current_string += ' '
                check = 'no_2'
            else:
                current_string += dict2[rnd.randrange(dict2_len)]
                current_string += ' '
                check = 'no_1'
        strings.append(current_string)

    return strings

def create_strings_from_wikipedia(minimum_length, count, lang):
    """
        Create all string by randomly picking Wikipedia articles and taking sentences from them.
    """
    sentences = []

    while len(sentences) < count:
        # We fetch a random page
        page = requests.get('https://{}.wikipedia.org/wiki/Special:Random'.format(lang))

        soup = BeautifulSoup(page.text, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        # Only take a certain length
        lines = list(filter(
            lambda s:
                len(s.split(' ')) > minimum_length
                and not "Wikipedia" in s
                and not "wikipedia" in s,
            [
                ' '.join(re.findall(r"[\w']+", s.strip()))[0:200] for s in soup.get_text().splitlines()
            ]
        ))

        # Remove the last lines that talks about contributing
        sentences.extend(lines[0:max([1, len(lines) - 5])])

    return sentences[0:count]

def create_strings_randomly(length, allow_variable, count, let, num, sym, lang):
    """
        Create all strings by randomly sampling from a pool of characters.
    """

    # If none specified, use all three
    if True not in (let, num, sym):
        let, num, sym = True, True, True

    pool = ''
    if let:
        if lang == 'cn':
            pool += ''.join([chr(i) for i in range(19968, 40908)]) # Unicode range of CHK characters
        else:
            pool += string.ascii_letters
    if num:
        pool += "0123456789"
    if sym:
        pool += "!\"#$%&'()*+,-./:;?@[\\]^_`{|}~"

    if lang == 'cn':
        min_seq_len = 1
        max_seq_len = 2
    else:
        min_seq_len = 2
        max_seq_len = 10

    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length) if allow_variable else length):
            seq_len = rnd.randint(min_seq_len, max_seq_len)
            current_string += ''.join([rnd.choice(pool) for _ in range(seq_len)])
            current_string += ' '
        strings.append(current_string[:-1])
    return strings


def create_strings_randomly_v2(length, allow_variable, count, let, num, sym, lang):
    """
        Create all strings by randomly sampling from a pool of characters.
    """

    # If none specified, use all three
    if True not in (let, num, sym):
        let, num, sym = True, True, True

    pool = ''

    if num:
        pool += "0123456789"
    if sym:
        pool += "!\"#$%&'()*+,-./:;?@[\\]^_`{|}~"


    min_seq_len = 1
    max_seq_len = 3

    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length) if allow_variable else length):
            seq_len = rnd.randint(min_seq_len, max_seq_len)
            current_string += ''.join([rnd.choice(pool) for _ in range(seq_len)])
            seq_len2 = rnd.randint(1, 1)
            if len(lang) >1 :
                if rnd.random() > 0.5:
                    current_string += ''.join([rnd.choice(lang[0]) for _ in range(seq_len2)])
                else:
                    current_string += ''.join([rnd.choice(lang[1]) for _ in range(seq_len2)])
            else:
                current_string += ''.join([rnd.choice(lang) for _ in range(seq_len2)])
            current_string += ' '
        strings.append(current_string[:-1])
    return strings