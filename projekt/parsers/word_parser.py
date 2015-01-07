#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
sys.path.append('../')

from strings.ngram import Ngram
import pandas as pd
from constans_file.constans import *

class WordsParser(object):
    def __init__(self, file_words):
        super(WordsParser, self).__init__()
        self.parse_data(file_words, csv_delimiter=CSV_DELIMITER)
    
    def parse_data(self, file_words, csv_delimiter=CSV_DELIMITER):
        df = pd.read_csv(file_words, csv_delimiter)
        self.words = self._sorted([Ngram(ngram,df.FreqSum[index]) for index, ngram in enumerate(df.Word) 
                                  if df.dlugosc[index] == 4]) 

    def _sorted(self, ngrams):
        return sorted(ngrams, key=lambda ngram: ngram.get_freq(), reverse=True)

    def get_words(self):
        return self.words
