import nltk
import sys
import os
import string
from nltk.tokenize import word_tokenize
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = dict()
    files = os.listdir(directory)
    for file in files:
        f = open(os.path.join(directory,file),"r",encoding="utf8")
        data[file] = f.read()
    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    stop_words = set(nltk.corpus.stopwords.words("english"))
    punctuations = string.punctuation
    words = word_tokenize(document)
    result= list()
    for word in words:
        if word not in stop_words and word not in punctuations:
            result.append(word)
    return result
    

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dict_count = 0
    idf = dict()
    words = []

    for doc in documents:
        for word in documents[doc]:
            words.append(word)
        dict_count+=1
    
    for word in words:
        count = 0
        for doc in documents:
            if word in documents[doc]:
                count+=1
        idf[word] = math.log(dict_count/count)  

    return idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = dict()
    
    for file in files:
        score = 0
        for word in files[file]:
            if word in idfs and word in query:
                score+=idfs[word]
        file_scores[file] = score

    sorted_files= sorted(file_scores.items(), key=lambda x:x[1],reverse=True)
    top_files = list()

    for i in range(0,n):
        top_files.append(sorted_files[i][0])

    return top_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = dict()
    
    for sentence in sentences:
        score = 0
        density = 0
        for word in sentences[sentence]:
            if word in query:
                density+=1
                if word in idfs:
                    score+=idfs[word]
        sentence_score[sentence] = (score,density)
    
    sorted_sentences= sorted(sentence_score.items(), key = lambda x:x[1],reverse=True)

    top_sentences = list()
    
    for i in range(0,n):
        top_sentences.append(sorted_sentences[i][0])
    
    return top_sentences

if __name__ == "__main__":
    main()
