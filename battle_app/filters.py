import enchant

en_US = enchant.Dict('en_US')
en_GB = enchant.Dict('en_GB')

AVAILABLE_LANGUAGES = (en_US, en_GB)

EXCLUDE_TYPES = ('$', "''", '(', ')', ',',
    '--', '.', ':', 'CC', 'CD', 'DT', 'EX',
    'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS',
    'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'SYM', 'TO')

TYPES = ('NN', 'ADV', 'ADJ')

EXCLUDE_WORDPARTS = ('http://', '//', 'https://', 'HTTP://', 'HTTPS://')
