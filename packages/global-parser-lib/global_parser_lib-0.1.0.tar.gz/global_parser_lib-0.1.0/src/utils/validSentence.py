import nltk
from nltk.data import find
from nltk import pos_tag, word_tokenize

nltk_resources_checked = False
# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger')

def check_nltk_resources():
    global nltk_resources_checked
    if not nltk_resources_checked:
        try:
            find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        try:
            find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')
        
        try:
            find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        try:
            find('tokenizers/averaged_perceptron_tagger_eng')

        except LookupError:
            nltk.download('averaged_perceptron_tagger_eng')

        
        nltk_resources_checked = True

def is_valid_sentence_nltk(sentence: str) -> bool:
    check_nltk_resources()
    words = word_tokenize(sentence)
    if len(words) == 0:
        return False
    pos_tags = pos_tag(words)
    has_subject = any(tag in ['NN', 'NNS', 'NNP', 'NNPS'] for word, tag in pos_tags)
    has_verb = any(tag.startswith('VB') for word, tag in pos_tags)
    return has_subject and has_verb



def is_valid_sentence_v2(sentence):
    check_nltk_resources()
    # Remove leading/trailing whitespace
    sentence = sentence.strip()
    
    # Check if sentence is empty
    if not sentence:
        return False
    
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)
    
    # Check for minimum word count (at least 5 words)
    if len(words) < 5:
        return False
    
    # Part of Speech tagging
    pos_tags = nltk.pos_tag(words)
    
    # Check for presence of at least one verb
    has_verb = any(tag.startswith('V') for _, tag in pos_tags)
    
    # Check for presence of a subject (noun or pronoun)
    has_subject = any(tag.startswith(('N', 'PRP')) for _, tag in pos_tags)
    
    # Ensure the sentence starts with a capital letter
    is_capitalized = sentence[0].isupper()
    
    # Ensure the sentence ends with proper punctuation
    ends_with_punctuation = sentence[-1] in '.?!'
    
    # Combine all checks
    return (has_verb and has_subject and 
            is_capitalized and ends_with_punctuation)


if __name__ == "__main__":
    print(is_valid_sentence_nltk("My Fone ringing"))