
import nltk

default_types = ['$', "''", '(', ')', ',',
    '--', '.', ':', 'CC', 'CD', 'DT', 'EX',
    'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS',
    'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'SYM', 'TO']


def exclude_by_type(text, word_types=default_types):
    """
    exclude items by type function
    """
    text = nltk.word_tokenize(text)
    text = list(set(text))
    text = nltk.pos_tag(text)
    cleaned_list = []
    for item in text:
        if item[1] not in word_types:
            cleaned_list.append(item[0])
    return cleaned_list