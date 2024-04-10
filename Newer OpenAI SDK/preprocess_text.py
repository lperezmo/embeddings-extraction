#------------------------------------#
# Import Libraries
#------------------------------------#
from tqdm.auto import tqdm
import nltk

#------------------------------------#
# Break text into chunks and clean
#------------------------------------#

def split_text_into_chunks(text, max_sentences=10):
    """
    Splits a long text into chunks of text, each with a maximum number of sentences.
    
    Parameters
    ----------
    text : str
    max_sentences : int, default=10
    
    Returns
    -------
    chunks : list of str
    """
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sentence_tokenizer.tokenize(text)

    total_sentences = len(sentences)
    start = 0
    chunks = []

    while start < total_sentences:
        end = min(start + max_sentences, total_sentences)
        chunk = ' '.join(sentences[start:end])
        chunks.append(chunk)
        start = end

    return chunks

def break_and_clean(extracted_text_data):
    """
    Breaks text into chunks and cleans it.
    
    Parameters
    ----------
    extracted_text_data : list of dict

    Returns
    -------
    new_data : list of dict
    """
    # Download the Punkt tokenizer if it's not already installed
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    # Break text into chunks
    new_data = []

    for data in extracted_text_data:
        chunks = split_text_into_chunks(data['text'])

        for chunk in chunks:
            new_item = data.copy()
            new_item['text'] = chunk
            new_data.append(new_item)

    # Clean up text (words are mixed together), restore spaces between words
    for data in new_data:
        data['text'] = data['text'].replace('\n', ' ')
        data['text'] = data['text'].replace('.', '')

    # # For each item in the dataset, remove the ".htm" at the end of the filename
    for data in new_data:
        data['file'] = data['file'][:-4]

    return new_data
