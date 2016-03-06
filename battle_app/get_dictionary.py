
import nltk
import requests

from .models import Word, Synonym, WordUsage

default_types = ['$', "''", '(', ')', ',',
    '--', '.', ':', 'CC', 'CD', 'DT', 'EX',
    'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS',
    'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'SYM', 'TO']

default_wordparts = ['http://', '//', 'https://', 'HTTP://', 'HTTPS://']


def exclude_by_type(text, word_types=default_types, wordparts=default_wordparts):
    """
    exclude items by type function
    """

    if type(text).__name__ != 'list':
        text = nltk.word_tokenize(text)
    text = list(set(text))
    text = nltk.pos_tag(text)
    cleaned_list = []
    for item in text:
        if item[1] not in word_types:
            cleaned_list.append(item[0])
    final_list = []
    for word in cleaned_list:
        for part in wordparts:
            if part not in word:
                final_list.append(word)
    return final_list

def create_synonyms(orig_word):
    try:
        headers = {
            "X-Mashape-Key": "aIder4iWr4msh5Scn073WRoddmAEp1qA0I3jsnSR8lfJwtyzpg",
            "Accept": "application/json"}

        response = requests.get("https://wordsapiv1.p.mashape.com/words/%s/synonyms" % orig_word, headers=headers)
        if response.status_code == 200:
            json = response.json()
            synonyms = json['synonyms']
            # synonyms = nltk.word_tokenize(synonyms)
            synonyms = nltk.pos_tag(synonyms)
            word = nltk.word_tokenize(orig_word)
            word = nltk.pos_tag(word)[0]
            print(synonyms)
            good_syns = []
            for syn in synonyms:
                print(word[1], syn[1])
                if word[1] == syn[1]:
                    print('*')
                    good_syns.append(syn[0])
            try:
                word = Word.objects.get(word=orig_word)
            except Word.DoesNotExist:
                word = Word.objects.create(word=orig_word)
            for syn in good_syns[:2]:
                try:
                    new_word = Word.objects.create(word=syn.lower(), is_synonym=True)
                except Exception:
                    new_word = Word.objects.get(word=word)
                syn = Synonym.objects.create(word=new_word)
                syn.synonym_to.add(word)
            return good_syns
    except Exception as e:
        print(e)


def analyze_post(text):
    text = text.split()
    text = list(set(text))
    final_text = []
    for word in text:
        word = Word.objects.get(word=word)
        word_stats = get_stats(word.word)
        final_word = word_stats
        synonims = Synonym.objects.filter(synonym_to=word)
        for syn in synonims:
            stats = get_stats(syn)
            if word_stats['success_rate'] < stats['success_rate']:
                stats['succes_rate'] = stats['success_rate'] / word_stats['success_rate']
                final_word = stats
        final_text.append(final_word)
    return final_text




def get_stats(word):
    stats = {}
    try:
        word_obj = Word.objects.get(word=word)
        usage = WordUsage.objects.filter(word=word_obj)
        count = usage.count()
        retweets = 0
        likes = 0
        for use in usage:
            retweets += use.retweets
            likes += use.likes
        likes_success = likes/count
        retweets_success = retweets/count
        rate = (likes_success + retweets_success)/2
        return {
            'word': word,
            'success_rate': rate}
    except Exception:
        return {'word': '',
            'success_rate': 0}