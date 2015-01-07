#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
sys.path.append('../')

from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
from strings.ngram import Ngram
from constans_file.constans import *


class NgramsParser(object):
    __metaclass__ = ABCMeta

    def __init__(self, file_middle_ngrams, file_edge_ngrams, 
                 csv_delimiter=CSV_DELIMITER):

        self.parse_data(file_middle_ngrams, file_edge_ngrams, csv_delimiter)

    def parse_data(self, file_middle_ngrams, file_edge_ngrams, csv_delimiter):
        self.middle_ngrams = self._parse_middle_engdams(file_middle_ngrams, 
                                                        csv_delimiter)

        self.start_ngrams, self.stop_ngrams = self._parse_edge_ngrams(file_edge_ngrams, 
                                                                      csv_delimiter)

    def _sorted(self, ngrams):
        return sorted(ngrams, key=lambda ngram: ngram.get_freq(), reverse=True)

    def _parse_middle_engdams(self, file_name, csv_delimiter):
        df = pd.read_csv(file_name, csv_delimiter)
        ngrams = self._sorted([Ngram(ngram,freq) for ngram,freq in zip(df.ngram,df.freq) 
                               if (not WORD_SEPARATOR in str(ngram) and \
                                  len(FORBIDDEN_CHARACTERS & set(ngram)) == 0)])

        return self._sorted(ngrams)

    def _parse_edge_ngrams(self, file_name, csv_delimiter):
        df = pd.read_csv(file_name, csv_delimiter)
        start_ngrams, stop_ngrams = [], []
        for ngram, freq in zip(df.ngram, df.freq):
            if str(ngram).count(WORD_SEPARATOR) == 1 and \
               len(FORBIDDEN_CHARACTERS & set(ngram)) == 0:

                if ngram[0] == WORD_SEPARATOR:
                    start_ngrams.append(Ngram(ngram, freq))

                elif ngram[-1] == WORD_SEPARATOR:
                    stop_ngrams.append(Ngram(ngram, freq))

        return self._sorted(start_ngrams), self._sorted(stop_ngrams)

    def _get_freq_ngrams(self, lower, upper, ngrams, ngrams_type):
        freq = [ngram.get_freq() for ngram in ngrams]
        if ngrams_type == 'rate':
            per_lower = np.percentile(freq,lower)
            lower_ngram = [ngram for ngram in ngrams 
                           if ngram.get_freq() < per_lower]

            return lower_ngram

        elif ngrams_type == 'middle':
            per_lower = np.percentile(freq,lower)
            per_upper = np.percentile(freq,upper)
            middle_ngram = [ngram for ngram in ngrams 
                            if ngram.get_freq() > per_lower and \
                            ngram.get_freq() < per_upper]

            return middle_ngram

        elif ngrams_type == 'frequent':
            per_upper = np.percentile(freq,upper)
            upper_ngram = [ngram for ngram in ngrams 
                           if ngram.get_freq() > per_upper]
            return upper_ngram

        else:
            raise Exception("Error: Wrong ngrams freq type \
                            (posible: rate, middle, frequent)")

    def get_start_ngrams(self):
        return self.start_ngrams

    def get_stop_ngrams(self):
        return self.stop_ngrams

    def get_middle_ngrams(self):
        return self.middle_ngrams

    @abstractmethod
    def get_ngrams(self):
        pass

    @abstractmethod
    def get_freq_ngrams(self, lower, upper):
        pass
