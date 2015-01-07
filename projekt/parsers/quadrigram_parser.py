#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division
from ngram_parser import NgramsParser

class QuadrigramsParser(NgramsParser):
    def __init__(self, file_middle_ngrams, file_ngrams):
        super(QuadrigramsParser, self).__init__(file_middle_ngrams, 
                                                file_ngrams)

    def get_ngrams(self):
        return self._sorted(self.get_start_ngrams()+
                            self.get_stop_ngrams()+
                            self.get_middle_ngrams())

    def get_freq_ngrams(self, lower, upper, ngrams_freq_type=''):
        return self._get_freq_ngrams(lower, 
                                     upper, 
                                     self.get_ngrams(), 
                                     ngrams_freq_type)
