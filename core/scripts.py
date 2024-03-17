from random import choice, shuffle


def get_words(set_of_words: set):
    set_of_words = list(set_of_words)
    get_four = set()

    while len(get_four) != 4:
        get_four.add(choice(set_of_words))

    return get_four


def get_samples(set_of_words: set):
    gen = (str(elem._asdict()['Word']).split(': ') for elem in set_of_words)
    gen = {x[0]: x[1] for x in gen}
    pair = choice(list(gen.items()))
    choices = list(gen.values())
    shuffle(choices)
    return pair, choices
