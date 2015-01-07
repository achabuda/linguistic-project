#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function, division
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
from itertools import permutations
from parsers.bigram_parser import BigramsParser
from parsers.quadrigram_parser import QuadrigramsParser
from parsers.unigram_parser import UnigramsParser
from parsers.word_parser import WordsParser
from strings.condition_string import ConditionString
from strings.ngram import Ngram
from constans_file.constans import *

'''
    Conditions:
    
        (1) strings of infrequent letters forming rare bigrams
        (2) strings of frequent letters forming rare bigrams
        (3) strings of frequent letters forming middle-frequency bigrams
        (4) strings of frequent letters forming frequent bigrams but rare quadrigrams
        (5) pseudowords (frequent letters forming frequent bigrams forming frequent quadrigrams)
        (6) words

    for each condition:
        seq1 - 60 strings with one brille target on position 2, 3 or 4 with one vowel
        seq2 - 60 strings with one brille target on position 2, 3 or 4 without vowels
        seq3 - 60 strings without brille target with one vowel
        seq4 - 60 strings without brille target without vowel

    brille taarget:
        letters: ą, b, c, i, e, k

    rare ngram: ngram_freq < 40'' 
    middle-frequency ngram: 40''< freq < 70''
    frequent ngram: 70''<freq

'''


class Condition(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        super(Condition, self).__init__()

    @abstractmethod
    def comput_sequens(self):
        pass

    def _filtr_ngrams_with_unigrams(self, ngrams, unigrams):
        use_unigrams = set([unigram.get_name() for unigram in unigrams])
        return [ngram for ngram in ngrams 
                if all([unigram in use_unigrams for unigram in ngram.get_name()])]

    def _comput_sequens_with_bigrams(self, start_bigrams, stop_bigrams, middle_bigrams): 
        bigrams = start_bigrams + stop_bigrams

        middle_bigrams_name = set([bigram.get_name() for bigram in 
                                   middle_bigrams])
        permutation = [p for p in permutations(bigrams,2) 
                       if p[0].get_type()=='ngram_start' and\
                       p[1].get_type()=='ngram_stop']
        #print(len(permutation))
        seq1, seq2, seq3, seq4 = [], [], [], []
        for p in permutation:
            condition_string = ConditionString(p)
            try:
                condition_string.add_freq([ngram.freq for ngram in middle_bigrams 
                                         if ngram.get_name() == condition_string.get_name()[1:3]][0])

                if condition_string.is_target() is True and \
                   condition_string.is_vovel() is True:

                    seq1.append(condition_string)

                elif condition_string.is_target() is True and \
                    condition_string.is_vovel() is False:

                    seq2.append(condition_string)

                elif condition_string.is_target() is False and \
                    condition_string.is_vovel() is True:

                    seq3.append(condition_string)

                elif condition_string.is_target() is False and \
                    condition_string.is_vovel() is False:

                    seq4.append(condition_string)
            except IndexError:

                pass
        return seq1, seq2, seq3, seq4

class ConditionBigrams(Condition):
    """Condition 1, 2, 3"""
    def __init__(self, unigrams, type_unigrams, bigrams, type_bigrams):
        super(Condition, self).__init__()
        if type_unigrams == 'infrequent':
            self.unigrams = unigrams.get_freq_ngrams(treshold_letter=TRESHOLD_LETTERS, 
                                                       treshold_type='lower')

        elif type_unigrams == 'frequent':
            self.unigrams = unigrams.get_freq_ngrams(treshold_letter=TRESHOLD_LETTERS, 
                                                       treshold_type='upper')

        else:
            raise Exception("Error: not specified the type of unigram \
                            (posible: infrequent, frequent")

        if type_bigrams == 'rate':
            self.start_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                         PERCENTAGLE_UPPER, 
                                                         ngrams_type='start', 
                                                         ngrams_freq_type='rate')

            self.stop_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='stop', 
                                                        ngrams_freq_type='rate')
            self.middle_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                          PERCENTAGLE_UPPER, 
                                                          ngrams_type='middle', 
                                                          ngrams_freq_type='rate')
        elif type_bigrams == 'middle':
            self.start_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                         PERCENTAGLE_UPPER, 
                                                         ngrams_type='start', 
                                                         ngrams_freq_type='middle')

            self.stop_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='stop', 
                                                        ngrams_freq_type='middle')

            self.middle_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                          PERCENTAGLE_UPPER, 
                                                          ngrams_type='middle', 
                                                          ngrams_freq_type='middle')

        elif type_bigrams == 'frequent':
            self.start_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='start', 
                                                        ngrams_freq_type='frequent')

            self.stop_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='stop', 
                                                        ngrams_freq_type='frequent')

            self.middle_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                          PERCENTAGLE_UPPER, 
                                                          ngrams_type='middle', 
                                                          ngrams_freq_type='frequent')
        else:
            raise Exception("Error: not specified the type of bigrams \
                            (posible: rate, middle, frequent ")

    def comput_sequens(self):
        self.start_bigrams = self._filtr_ngrams_with_unigrams(self.start_bigrams, 
                                                              self.unigrams)

        self.stop_bigrams = self._filtr_ngrams_with_unigrams(self.stop_bigrams, 
                                                             self.unigrams)

        self.middle_bigrams = self._filtr_ngrams_with_unigrams(self.middle_bigrams, 
                                                               self.unigrams)

        return self._comput_sequens_with_bigrams(self.start_bigrams, 
                                                 self.stop_bigrams, 
                                                 self.middle_bigrams)

class ConditionQuadrigrams(Condition):
    """Condition 4, 5"""
    def __init__(self, unigrams, type_unigrams, bigrams, type_bigrams, 
                 quadrigrams, type_quadrigrams, words):
        super(Condition, self).__init__()

        if type_unigrams == 'infrequent':
            self.unigrams = unigrams.get_freq_ngrams(treshold_letter=TRESHOLD_LETTERS, 
                                                       treshold_type='lower')

        elif type_unigrams == 'frequent':
            self.unigrams = unigrams.get_freq_ngrams(treshold_letter=TRESHOLD_LETTERS, 
                                                    treshold_type='upper')

        else:
            raise Exception("Error: not specified the type of unigram \
                            (posible: infrequent, frequent)")

        if type_bigrams == 'rate':
            self.start_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                         PERCENTAGLE_UPPER, 
                                                         ngrams_type='start', 
                                                         ngrams_freq_type='rate')

            self.stop_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='stop', 
                                                        ngrams_freq_type='rate')

            self.middle_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='middle', 
                                                        ngrams_freq_type='rate')

        elif type_bigrams == 'middle':
            self.start_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                         PERCENTAGLE_UPPER, 
                                                         ngrams_type='start', 
                                                         ngrams_freq_type='middle')

            self.stop_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='stop', 
                                                        ngrams_freq_type='middle')

            self.middle_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                          PERCENTAGLE_UPPER, 
                                                          ngrams_type='middle', 
                                                          ngrams_freq_type='middle')

        elif type_bigrams == 'frequent':
            self.start_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                         PERCENTAGLE_UPPER, 
                                                         ngrams_type='start', 
                                                         ngrams_freq_type='frequent')

            self.stop_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                        PERCENTAGLE_UPPER, 
                                                        ngrams_type='stop', 
                                                        ngrams_freq_type='frequent')

            self.middle_bigrams = bigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                          PERCENTAGLE_UPPER, 
                                                          ngrams_type='middle', 
                                                          ngrams_freq_type='frequent')
        else:
            raise Exception("Error: not specified the type of bigrams \
                            (posible: rate, middle, frequent)")

        if type_quadrigrams == 'rate':
            self.quadrigrams = quadrigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                           PERCENTAGLE_UPPER, 
                                                           ngrams_freq_type='rate')

        elif type_quadrigrams == 'middle':
            self.quadrigrams = quadrigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                           PERCENTAGLE_UPPER, 
                                                           ngrams_freq_type='middle')

        elif type_quadrigrams == 'frequent':
            self.quadrigrams = quadrigrams.get_freq_ngrams(PERCENTAGLE_LOWER, 
                                                           PERCENTAGLE_UPPER, 
                                                           ngrams_freq_type='frequent')

        else:
            raise Exception("Error: not specified the type of quadrigrams \
                            (posible: rate, middle, frequent)")

        self.words = words.get_words()

    def comput_sequens(self):
        self.start_bigrams = self._filtr_ngrams_with_unigrams(self.start_bigrams, 
                                                              self.unigrams)

        self.stop_bigrams = self._filtr_ngrams_with_unigrams(self.stop_bigrams, 
                                                             self.unigrams)

        self.middle_bigrams = self._filtr_ngrams_with_unigrams(self.middle_bigrams, 
                                                               self.unigrams)

        seq1, seq2, seq3, seq4 =  self._comput_sequens_with_bigrams(self.start_bigrams, 
                                                                    self.stop_bigrams, 
                                                                    self.middle_bigrams)

        quadrigrams = [quadrigram.get_name() for quadrigram in self.quadrigrams]
        words  = [word.get_name() for word in self.words]
        for seq in [seq1, seq2, seq3, seq4]:
            for condition_string in seq:
                if not((condition_string.get_name() in quadrigrams) and \
                       (condition_string.get_name() not in words)):

                    seq.remove(condition_string)

        return seq1, seq2, seq3, seq4

class ConditionWords(Condition):
    """Condition 6"""
    def __init__(self, unigram, type_unigram, words):
        super(Condition, self).__init__()

        if type_unigram == 'infrequent':
            self.unigrams = unigrams.get_freq_ngrams(treshold_letter=TRESHOLD_LETTERS, 
                                                       treshold_type='lower')
        elif type_unigram == 'frequent':
            self.unigrams = unigrams.get_freq_ngrams(treshold_letter=TRESHOLD_LETTERS, 
                                                       treshold_type='upper')
        elif type_unigram == '':
            self.unigrams = unigrams.get_ngrams()
            pass
        else:
            raise Exception("Error: not specified the type of unigram \
                            (posible: infrequent, frequent)")
        self.words = words.get_words()

    def comput_sequens(self):
        self.words = self._filtr_ngrams_with_unigrams(self.words, self.unigrams)
        seq1, seq2, seq3, seq4 = [], [], [], []
        for word in self.words:
            condition_string = ConditionString([word,Ngram('', 0)])
            if condition_string.is_target() is True and \
               condition_string.is_vovel() is True:

                seq1.append(condition_string)

            elif condition_string.is_target() is True and \
                 condition_string.is_vovel() is False:

                seq2.append(condition_string)

            elif condition_string.is_target() is False and \
                 condition_string.is_vovel() is True:

                seq3.append(condition_string)

            elif condition_string.is_target() is False and \
                 condition_string.is_vovel() is False:

                seq4.append(condition_string)

        return seq1, seq2, seq3, seq4

def write_to_csv(condition_name,data):
    df = pd.DataFrame({'ngram': [x.name.encode(CODING) for x in data],'freq1': [x.freq[0] for x in data], 'freq2': [x.freq[2] for x in data], 'freq3': [x.freq[1] for x in data]})

    df.to_csv(condition_name ,sep=',')

def write_to_csv2(condition_name,data):
    df = pd.DataFrame({'ngram': [x.name.encode(CODING) for x in data],'freq': [x.freq[0] for x in data]})
    df.to_csv(condition_name ,sep=',')



if __name__ == '__main__':
    file_birams = "./data/bigrams.csv"
    file_trigrams = "./data/trigrams.csv"
    file_quadrigrams = "./data/quadrigrams.csv"
    file_pentagrams = "./data/pentagrams.csv"
    file_unigrams = "./data/unigrams.csv"
    file_words = "./data/słowa.csv"
    unigrams = UnigramsParser(file_unigrams)
    bigrams = BigramsParser(file_birams, file_trigrams)
    quadrigrams = QuadrigramsParser(file_quadrigrams, file_pentagrams)
    words = WordsParser(file_words)

    # #CONDITION 1
    # condition1 = ConditionBigrams(unigrams, "infrequent", bigrams, "rate").comput_sequens()
    # # write_to_csv("condition1_seq1",condition1[0])
    # # write_to_csv("condition1_seq2",condition1[1])
    # # write_to_csv("condition1_seq3",condition1[2])
    # # write_to_csv("condition1_seq4",condition1[3])
    # # #CONDITION 2
    # condition2 = ConditionBigrams(unigrams, "frequent", bigrams, "rate").comput_sequens()
    # # write_to_csv("condition2_seq1",condition2[0])
    # # write_to_csv("condition2_seq2",condition2[1])
    # # write_to_csv("condition2_seq3",condition2[2])
    # # write_to_csv("condition2_seq4",condition2[3])
    # # # #CONDITION 3
    # condition3 = ConditionBigrams(unigrams, "frequent", bigrams, "middle").comput_sequens()
    # # write_to_csv("condition3_seq1",condition3[0])
    # # write_to_csv("condition3_seq2",condition3[1])
    # # write_to_csv("condition3_seq3",condition3[2])
    # # write_to_csv("condition3_seq4",condition3[3])
    # # # #CONDITION 4
    # condition4 = ConditionQuadrigrams(unigrams, "frequent", bigrams, "frequent", quadrigrams, "rate", words).comput_sequens()
    # # write_to_csv("condition4_seq1",condition4[0])
    # # write_to_csv("condition4_seq2",condition4[1])
    # # write_to_csv("condition4_seq3",condition4[2])
    # # write_to_csv("condition4_seq4",condition4[3])
    # # # #CONDITION 5
    # condition5 = ConditionQuadrigrams(unigrams, "frequent", bigrams, "frequent", quadrigrams, "frequent", words).comput_sequens()
    # # write_to_csv("condition5_seq1",condition4[0])
    # # write_to_csv("condition5_seq2",condition4[1])
    # # write_to_csv("condition5_seq3",condition4[2])
    # # write_to_csv("condition5_seq4",condition4[3])
    # # # #CONDITION 6
    condition6 = ConditionWords(unigrams, "", words).comput_sequens()
    write_to_csv2("condition6_seq1",condition6[0])
    write_to_csv2("condition6_seq2",condition6[1])
    write_to_csv2("condition6_seq3",condition6[2])
    write_to_csv2("condition6_seq4",condition6[3])
