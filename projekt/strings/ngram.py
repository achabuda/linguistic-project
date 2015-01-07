#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
sys.path.append('../')

from constans_file.constans import *

class Ngram(object):
    def __init__(self, name, freq):
        super(Ngram, self).__init__()
        self.name = name.decode(CODING).strip(WORD_SEPARATOR)
        self.freq = float(freq)
        self.type = self._get_type(name)

        self.target = self._get_target()
        self.vovel = self._get_vovel()

    def __str__(self):
        return (self.get_name().encode(CODING), 
                self.get_freq(), 
                self.get_type())

    def __repr__(self):
        return repr((self.get_name().encode(CODING), 
                     self.get_freq(), 
                     self.get_type()))

    def _get_type(self, name):
        if name.find(WORD_SEPARATOR) == 0:
            return 'ngram_start'

        elif name.find(WORD_SEPARATOR) == -1:
            return 'ngram_middle'

        else:
            return 'ngram_stop'

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_freq(self):
        return self.freq

    def _get_target(self):
        target = sum([t for t in [self.name.count(target) for target in BRILLE_LETTERS]])
        if target == 1:
            return True
        elif target == 0:
            return False
        else:
            return None

    def _get_vovel(self):
        vovel = sum([t for t in [self.name.count(target) for target in VOLVES]])
        if vovel == 1:
            return True
        elif vovel == 0:
            return False
        else:
            return None

    def is_target(self):
        return self.target

    def is_vovel(self):
        return self.vovel
