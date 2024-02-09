import sys
from collections import defaultdict
import itertools
import math
import random
import os
import os.path

'''
COMS W4705 - Natural Language Processing - Summer 2020 
Homework 1 - Programming Component: Trigram Language Models
Daniel Bauer
'''


def corpus_reader(corpusfile, lexicon=None):
    with open(corpusfile, 'r') as corpus:
        for line in corpus:
            if line.strip():
                sequence = line.lower().strip().split()
                if lexicon:
                    yield [word if word in lexicon else 'UNK' for word in sequence]
                else:
                    yield sequence


def get_lexicon(corpus):
    word_counts = defaultdict(int)
    for sentence in corpus:
        for word in sentence:
            word_counts[word] += 1
    return set(word for word in word_counts if word_counts[word] > 1)


def get_ngrams(sequence, n):
    '''
    COMPLETE THIS FUNCTION (PART 1)
    Given a sequence, this function should return a list of n-grams, where each n-gram is a Python tuple.
    This should work for arbitrary values of 1 <= n < len(sequence).
    '''

    if n > 1:
        sequence = ['START'] * (n - 1) + sequence
    else:
        sequence = ['START'] + sequence
    sequence += ['STOP']
    ngrams = []
    for i in range(len(sequence) - n + 1):
        ngrams.append(tuple(sequence[i:i + n]))
    return ngrams


class TrigramModel(object):

    def __init__(self, corpusfile):

        # Iterate through the corpus once to build a lexicon
        generator = corpus_reader(corpusfile)
        self.lexicon = get_lexicon(generator)
        self.lexicon.add('UNK')
        self.lexicon.add('START')
        self.lexicon.add('STOP')
        self.num_sentences = 0  # keep track of the number of sentences

        # Now iterate through the corpus again and count ngrams
        generator = corpus_reader(corpusfile, self.lexicon)
        self.count_ngrams(generator)
        self.total_num_words = sum(count for gram, count in self.unigramcounts.items()) - self.unigramcounts[('START',)]

    def count_ngrams(self, corpus):
        '''
        COMPLETE THIS METHOD (PART 2)
        Given a corpus iterator, populate dictionaries of unigram, bigram,
        and trigram counts.
        '''

        self.unigramcounts = defaultdict(int)  # might want to use defaultdict or Counter instead
        self.bigramcounts = defaultdict(int)
        self.trigramcounts = defaultdict(int)

        ##Your code here
        for sent in corpus:
            self.num_sentences += 1
            unigrams = get_ngrams(sent, 1)
            for gram in unigrams:
                self.unigramcounts[gram] += 1
            bigrams = get_ngrams(sent, 2)
            for gram in bigrams:
                self.bigramcounts[gram] += 1
            trigrams = get_ngrams(sent, 3)
            for gram in trigrams:
                self.trigramcounts[gram] += 1

    def raw_trigram_probability(self, trigram):
        '''
        COMPLETE THIS METHOD (PART 3)
        Returns the raw (unsmoothed) trigram probability
        '''
        context = (trigram[0], trigram[1])
        if context == ('START', 'START'):
            # P(START, START, w) = P(START | w)
            return self.raw_bigram_probability((trigram[1], trigram[2]))

        trigram_count = self.trigramcounts[trigram]

        if trigram_count == 0:
            # We don't know anything about the distribution of the trigram[2]
            # in the context of trigram[0], trigram[1] -- assume
            #  uniform distribution
            return 1 / self.total_num_words

        elif self.bigramcounts[context] == 0:
            return self.raw_unigram_probability(trigram[2])

        return trigram_count / float(self.bigramcounts[context])

    def raw_bigram_probability(self, bigram):
        '''
        COMPLETE THIS METHOD (PART 3)
        Returns the raw (unsmoothed) bigram probability
        '''
        if self.unigramcounts[(bigram[0],)] == 0:
            return self.bigramcounts[bigram] / float(self.total_num_words)

        return self.bigramcounts[bigram] / float(self.unigramcounts[(bigram[0],)])

    def raw_unigram_probability(self, unigram):
        '''
        COMPLETE THIS METHOD (PART 3)
        Returns the raw (unsmoothed) unigram probability.
        '''

        # hint: recomputing the denominator every time the method is called
        # can be slow! You might want to compute the total number of words once,
        # store in the TrigramModel instance, and then re-use it.
        if unigram == ('START',):
            return 0
        return self.unigramcounts[unigram] / self.total_num_words

    def generate_sentence(self, t=20):
        '''
        COMPLETE THIS METHOD (OPTIONAL)
        Generate a random sentence from the trigram model. t specifies the
        max length, but the sentence may be shorter if STOP is reached.
        '''
        return result

    def smoothed_trigram_probability(self, trigram):
        '''
        COMPLETE THIS METHOD (PART 4)
        Returns the smoothed trigram probability (using linear interpolation).
        '''
        lambda1 = 1 / 3.0
        lambda2 = 1 / 3.0
        lambda3 = 1 / 3.0
        smoothed_prob = lambda1 * self.raw_trigram_probability(trigram) + \
                        lambda2 * self.raw_bigram_probability((trigram[1], trigram[2])) + \
                        lambda3 * self.raw_unigram_probability((trigram[2],))
        return smoothed_prob

    def sentence_logprob(self, sentence):
        '''
        COMPLETE THIS METHOD (PART 5)
        Returns the log probability of an entire sequence.
        '''
        trigrams = get_ngrams(sentence, 3)
        return sum(math.log2(self.smoothed_trigram_probability(trigram)) for trigram in trigrams)

    def perplexity(self, corpus):
        '''
        COMPLETE THIS METHOD (PART 6)
        Returns the log probability of an entire sequence.
        '''
        corpus, corpus_copy = itertools.tee(corpus)
        logprob_all_sents = sum(self.sentence_logprob(sent) for sent in corpus)
        total_words_in_corpus = sum(len(sent) + 1 for sent in corpus_copy)
        perp = 2 ** (-logprob_all_sents / float(total_words_in_corpus))
        return perp


def essay_scoring_experiment(training_file1, training_file2, testdir1, testdir2):
    # Part 7
    model1 = TrigramModel(training_file1)
    model2 = TrigramModel(training_file2)

    total = 0
    correct = 0

    for f in os.listdir(testdir1):
        pp1 = model1.perplexity(corpus_reader(os.path.join(testdir1, f), model1.lexicon))
        pp2 = model2.perplexity(corpus_reader(os.path.join(testdir1, f), model2.lexicon))
        total += 1
        if pp1 <= pp2:
            correct += 1

    for f in os.listdir(testdir2):
        pp1 = model1.perplexity(corpus_reader(os.path.join(testdir2, f), model1.lexicon))
        pp2 = model2.perplexity(corpus_reader(os.path.join(testdir2, f), model2.lexicon))
        total += 1
        if pp2 <= pp1:
            correct += 1
    return float(correct) / total


if __name__ == '__main__':
    # model = TrigramModel(sys.argv[1])

    # put test code here...
    # or run the script from the command line with
    # $ python -i trigram_model.py [corpus_file]
    # >>>
    #
    # you can then call methods on the model instance in the interactive
    # Python prompt.

    # Testing perplexity:
    # dev_corpus = corpus_reader(sys.argv[2], model.lexicon)
    # pp = model.perplexity(dev_corpus)
    # print('Perplexity', pp)

    # Essay scoring experiment:
    acc = essay_scoring_experiment('ets_toefl_data/train_high.txt', 'ets_toefl_data/train_low.txt',
                                   'ets_toefl_data/test_high', 'ets_toefl_data/test_low')
    print(acc)
