#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division
from ngram_parser import NgramsParser

class BigramsParser(NgramsParser):
    def __init__(self, file_middle_ngrams, file_ngrams):
        super(BigramsParser, self).__init__(file_middle_ngrams, file_ngrams)

    def get_ngrams(self, ngrams_type):
        if ngrams_type =='start':
            return self.get_start_ngrams()

        elif ngrams_type =='stop':
            return self.get_stop_ngrams()

        elif ngrams_type =='middle':
            return self.get_middle_ngrams()

        else:
            raise Exception("Error: Wrong ngrams type (posible: start, stop, middle)")

    def get_freq_ngrams(self, lower, upper, ngrams_type='', ngrams_freq_type=''):
        return self._get_freq_ngrams(lower, 
                                     upper, 
                                     self.get_ngrams(ngrams_type), 
                                     ngrams_freq_type)
    def find_bigram(self, ngram_name):
        try:
            return [ngram for ngram in self.get_middle_ngrams() 
                    if ngram.name == ngram_name][0]
        except IndexError:
            raise Exception("Middle bigram don't exist")

