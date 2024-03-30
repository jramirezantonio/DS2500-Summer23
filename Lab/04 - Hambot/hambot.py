"""
    Josue Antonio
    DS2500: Lab 4 - Hambot
    05/25/2023
"""

import re
import random

def read_lyrics(filename):
    ''' Function: read_lyrics
        Parameters: filename, a string
        Returns: a list of strings, one string per line
                (removes characters' names, punctuation,
                 and makes everything lowercase)
    '''
    all_lines = []
    
    infile =  open(filename, encoding='utf-8', errors='ignore')
    for line in infile:
        line = line.strip() # Removing leading/trailing whitespace
        line = re.sub('\[.*\]', '', line) # Remove character heading
        line = re.sub('[^\w\s]', '', line) # Remove punctuation
        line = line.lower() # convert to lower case
            
        if line != '':
            all_lines.append(line)

    infile.close()
    return all_lines

def make_startstop(lines):
    """ Create lists of start and stop words """
    start = []
    stop = []
    for lyric in lines:
        words = lyric.split()
        if len(words) != 1:
            start.append(words[0])
            stop.append(words[len(words) - 1])
    return start,stop

def make_startstop_tuples(lines):
    """ Create list of startword/stopword pais """
    pairs = []
    for lyric in lines:
        split = lyric.split()
        if len(split) >= 3:
            for i in range(len(split) - 2):
                pairs.append((split[i], split[i+2]))
    return pairs

def make_ngrams(lines):
    ''' Function: make_ngrams
        Parameters: list of lines (strings)
        Returns: dictionary of key = word, value = list of words that follow
    '''
    ngrams = {}
    for lyric in lines:
        split = lyric.split()
        for i in range(len(split) - 1):
            current_word = split[i]
            next_word = split[i + 1]
            if current_word in ngrams.keys():
                ngrams[current_word].append(next_word)
            else:
                ngrams.setdefault(current_word, []).append(next_word)
    return ngrams

def make_3grams(lines):
    ''' Function: make_3_grams
        Parameters: list of lines (strings)
        Returns: dictionary of key = (start_word, stop_word), value = list of words that could be between pair
    '''
    ngrams = {}
    for lyric in lines:
        split = lyric.split()
        if len(split) >= 3:
            for i in range(len(split) - 2):
                start_word = split[i]
                stop_word = split[i+2]
                middle_word = split[i+1]
                ngrams.setdefault((start_word, stop_word), []).append(middle_word)
    return ngrams

def generate_lyric(maxlen, start, stop, ngrams):
    ''' Function: generate_lyric
        Parameters: max length, list of start-words, list of stop-words,
                    dictionary of key = word, value = list of followed-by
        Returns: one line of Hamilton lyric
    '''
    curr_word = random.choice(start)
    lyric = curr_word

    while len((lyric.split())) < maxlen - 1:
        next_word = random.choice(ngrams[curr_word])
        if next_word in stop:
            lyric = lyric + ' ' + next_word
        else:
            following_word = random.choice(ngrams[next_word])
            lyric = lyric + ' ' + next_word + ' ' + following_word
    return lyric

def gen_lyric_3gram(maxlen, pairs, ngrams):
    ''' Function: gen_lyric_3gram
        Parameters: max length, list of startword/stopword pairs,
                    dictionary of key = word, value = list of followed-by
        Returns: one line of Hamilton lyric
    '''
    lyric = ''
    while len(lyric.split()) < maxlen:
        curr_pair = random.choice(pairs)
        mid_word = random.choice(ngrams[curr_pair])
        lyric = lyric + ' ' + curr_pair[0] + ' ' + mid_word + ' ' + curr_pair[1]

    return lyric


def generate_lyrics(n, maxlen, start, stop, ngrams):
    ''' Generate n lyrics using generate_lyric function '''
    lyrics = ""
    for i in range(n):
        lyrics += generate_lyric(maxlen, start, stop, ngrams) + '\n'
    return lyrics

def generate_3lyrics(n, maxlen, pairs, ngrams):
    ''' Generate n lyrics using gen_lyric_3gram function '''
    lyrics = ""
    for i in range(n):
        lyrics += gen_lyric_3gram(maxlen, pairs, ngrams) + '\n'
    return lyrics

def main():
    # Read data - store hamilton lyrics
    lines = read_lyrics('hamilton_lyrics.txt')

    # Create start, stop lists, and 2-grams dict
    start, stop = make_startstop(lines)
    grams = make_ngrams(lines)

    # Communication - print out generated lyrics for Hamilton using 2-grams
    lyrics = generate_lyrics(100, 50, start, stop, grams)
    print('2-grams lyrics:\n', lyrics)

    # Create start/stop pairs, and 3-grams dict
    ngrams = make_3grams(lines)
    pairs = make_startstop_tuples(lines)

    # Communication - print out generated lyrics for Hamilton using 3-grams
    three_lyrics = generate_3lyrics(100, 50, pairs, ngrams)
    print('3-grams lyrics:\n', three_lyrics)

"""
2-grams best lyric: everybodys dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and dancin and
3-grams best lyric: five six seven horses of course a million things whatd i miss the british forces when you try to our partnership but hamilton forgets go back to the record straight remain relentless til havent met him if you had you havent met create yeah keep anyone bargained for to new york
"""
if __name__ == '__main__':
    main()