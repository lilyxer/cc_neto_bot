from random import choice, shuffle


def get_words(set_of_words: set) -> set:
    """принимает множество из пар слово-перевод,
    возвращает множество из 4 рандомных пар слово-перевод"""
    set_of_words = list(set_of_words)
    get_four = set()

    while len(get_four) != 4:
        get_four.add(choice(set_of_words))

    return get_four


def get_samples(set_of_words: set) -> tuple:
    """на вход принимает множестов из 4 пар слово - перевод (тип Word)
    возвращаем кортеж из загаданого слово-перевод и 4 варианта ответа
    """
    gen = (str(elem._asdict()['Word']).split(': ') for elem in set_of_words)
    gen = {x[0]: x[1] for x in gen}
    pair = choice(list(gen.items()))
    choices = list(gen.values())
    shuffle(choices)
    return pair, choices

def parse_words(stroke: str):
    return (w.strip().capitalize() for w in stroke.split('-'))