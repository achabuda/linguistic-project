#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
sys.path.append('../')

from strings.ngram import Ngram
from constans_file.constans import *
import pandas as pd


class UnigramsParser(object):
    def __init__(self, file_unigrams, csv_delimiter=CSV_DELIMITER):
        self.parse_data(file_unigrams, csv_delimiter=CSV_DELIMITER)
    
    def parse_data(self, file_unigrams, csv_delimiter=CSV_DELIMITER):
        df = pd.read_csv(file_unigrams, csv_delimiter)
        self.unigrams = self._sorted([Ngram(ngram,freq) for ngram,freq in zip(df.ngram,df.freq) 
                                     if not ngram.isdigit()]) 

    def _sorted(self, ngrams):
        return sorted(ngrams, key=lambda ngram: ngram.get_freq(), reverse=True)

    def get_ngrams(self):
        return self.unigrams

    def get_freq_ngrams(self, treshold_letter='', treshold_type='lower'):
        if len(treshold_letter) != 0:
            if treshold_type == 'upper':
                letters = [unigram.get_name() for unigram in self.get_ngrams()]
                to_letter = letters.index(treshold_letter)
                return self.unigrams[:to_letter+1]
            elif treshold_type == 'lower':
                letters = [unigram.get_name() for unigram in self.get_ngrams()]
                from_letter = letters.index(treshold_letter)
                return self.unigrams[from_letter:]
            else:
                raise Exception("Error: not specified the type of threshold \
                                (posible: upper,lower)")
        else:
            raise Exception("Error: not specified the threshold \
                            (posible: letter)")
