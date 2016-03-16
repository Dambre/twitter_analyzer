
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
    '''
    funation for creating synonyms by passing word
    '''
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


class TextAnalysis(object):
    """Text analysis class"""
    def __init__(self, text, max_length):
        super(TextAnalysis, self).__init__()
        self._text = text
        self._max_length = max_length
        self._analized_text = None
        self._statistics = {}
        self._words = []
        self._improved_text = ''

    @property
    def text(self):
        return self._text

    @property
    def words(self):
        return list(set(nltk.word_tokenize(self.text)))

    @property
    def text_tokenized(self):
        return nltk.word_tokenize(self.text)
    
    @property
    def max_length(self):
        return self._max_length
    
    @property
    def analyzed_text(self):
        return self._analized_text
    
    @property
    def statistics(self):
        return self._statistics    

    @property
    def improved_text(self):
        return self._improved_text
    
    def get_synonyms(self, word_obj):
        return Synonym.objects.filter(synonym_to=word_obj)

    def get_or_create_word(self, word):
        try:
            word_obj = Word.objects.get(word=word)
        except Word.DoesNotExist:
            word_obj = Word.objects.create(word=word)
        return word_obj
            
    def get_all_words_with_synonyms(self):
        all_synonyms = []
        for word in self.words:
            word_obj = self.get_or_create_word(word)
            synonyms = self.get_synonyms(word_obj)
            for syn in synonyms:
                all_synonyms.append(syn.word.word)
        return list(set(self.words + all_synonyms))


    def get_stats_dict(
        self, count=0, retweets_rate=0, likes_rate=0,
        likes=0, retweets=0, rate=0):
        return {
            'retweets_rate': retweets_rate,
            'likes_rate': likes_rate,
            'usage_count': count,
            'likes_count': likes,
            'retweets_count': retweets,
            'rate': rate,
            }

    def get_stats(self, word):
        stats = {}
        try:
            usage = WordUsage.objects.filter(word=word)
            count = usage.count()
            retweets = 0
            likes = 0
            for use in usage:
                retweets += use.retweets
                likes += use.likes
            
            likes_rate = likes/count
            retweets_rate = retweets/count
            rate = (likes_rate + retweets_rate)/2
            return self.get_stats_dict(
                count, retweets_rate, likes_rate,
                likes, retweets, rate
                )
        except WordUsage.DoesNotExist:
            return self.get_stats_dict()

        except Exception:
            return self.get_stats_dict()

    def get_better_word(self, word_obj):
        synonyms = self.get_synonyms(word_obj)
        word_rate = self.statistics[word_obj.word]['rate']
        better_word = ''
        for syn in synonyms:
            if word_rate < self.statistics[syn.word.word]['rate']:
                better_word = syn.word.word
        return better_word
    
    def analyze_words(self):
        text = nltk.word_tokenize(self.text)
        analyzed_text = []
        all_words_with_synonyms = self.get_all_words_with_synonyms()
        for word in all_words_with_synonyms:
            word_obj = self.get_or_create_word(word)
            word_stats = self.get_stats(word_obj)
            self._statistics[word] = word_stats

    def analyze_text(self):
        self.analyze_words()

    def improve_text(self):   
        for word in self.text_tokenized:
            word_obj = self.get_or_create_word(word)
            better_word = self.get_better_word(word_obj)
            if better_word:
                self._improved_text += better_word + ' '
            else:
                self._improved_text += word + ' '

    def run(self):
        self.analyze_text()
        self.improve_text()
