import re
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('words')

def normalize_text(text):
    toko_tokenizer = ToktokTokenizer()
    wordnet_lemmatizer = WordNetLemmatizer()
    puncts = ['/', ',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£', 
        '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…', 
        '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', 
        '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', 
        '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√', ]

    def clean_text(text):
        text = str(text)
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        text = text.replace('/', ' ')
        for punct in puncts:
            if punct in text:
                text = text.replace(punct, '')
        return text.lower()

    def remove_duplicates(text):
        text = text.split(" ")
        for i in range(0, len(text)):
            text[i] = "".join(text[i])
        UniqW = Counter(text)
        text = " ".join(UniqW.keys())
        return text

    def clean_numbers(text):
        if bool(re.search(r'\d', text)):
            text = re.sub('[0-9]{5,}', '#####', text)
            text = re.sub('[0-9]{4}', '####', text)
            text = re.sub('[0-9]{3}', '###', text)
            text = re.sub('[0-9]{2}', '##', text)
        return text

    contraction_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",  "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as", "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",  "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have","you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have", "you're": "you are", "you've": "you have"}

    def _get_contractions(contraction_dict):
        contraction_re = re.compile('(%s)' % '|'.join(contraction_dict.keys()))
        return contraction_dict, contraction_re

    contractions, contractions_re = _get_contractions(contraction_dict)

    def replace_contractions(text):
        def replace(match):
            return contractions[match.group(0)]
        return contractions_re.sub(replace, text)

    def remove_stopwords(text, is_lower_case=True):
        stop_words = stopwords.words('english')
        stop_words.extend(['subreddit', 'subreddits', 'reddit', 'sub', 'nan']) # Remove reddit related words
        stop_words.extend(['question','like', 'post', 'find', 'finding', 'help', 'want', 'look', 'ask', 'people', 'something', 'thing', 'community', 'talk']) # Remove helper words
        stop_words.extend(['http', 'com', 'ww']) # Remove link
        tokens = toko_tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in stop_words]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
        filtered_text = ' '.join(filtered_tokens)    
        return filtered_text

    def lemmatizer(text):
        tokens = toko_tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        tokens = [wordnet_lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(tokens)

    def trim_text(text):
        tokens = toko_tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        return ' '.join(tokens)

    text_norm = clean_text(text)
    text_norm = remove_duplicates(text_norm)
    text_norm = clean_numbers(text_norm)
    text_norm = replace_contractions(text_norm)
    text_norm = remove_stopwords(text_norm)
    text_norm = lemmatizer(text_norm)
    text_norm = trim_text(text_norm)
    return text_norm