#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

import sys
sys.path.append('../')

from constans_file.constans import *

class ConditionString(object):
    def __init__(self, parts_string):
        super(ConditionString, self).__init__()
        self.name = "".join([part.name for part in parts_string])
        self.freq = [part.freq for part in parts_string ]
        self.target = self._get_target(parts_string)
        self.vovel = self._get_vovel(parts_string)

    def __str__(self):
        return "[{}, {}]".format(self.get_name().encode(CODING), 
                self.get_freq())

    def __repr__(self):
        return repr((self.get_name().encode(CODING), 
                     self.get_freq()))

    def _get_target(self, parts_string):
        if parts_string[0].is_target() is True and \
           parts_string[1].is_target() is False :
           return True
        elif parts_string[0].is_target() is False and \
            parts_string[1].is_target() is True :
            return True
        elif parts_string[0].is_target() is False and \
            parts_string[1].is_target() is False :
            return False
        else:
            return None

    def is_target(self):
        return self.target

    def _get_vovel(self, parts_string):
        if parts_string[0].is_vovel() is True and \
           parts_string[1].is_vovel() is False :
           return True
        elif parts_string[0].is_vovel() is False and \
            parts_string[1].is_vovel() is True :
            return True
        elif parts_string[0].is_vovel() is False and \
            parts_string[1].is_vovel() is False :
            return False
        else:
            return None

    def is_vovel(self):
        return self.vovel

    def get_name(self):
        return self.name

    def get_freq(self):
        return self.freq

    def add_freq(self, freq):
        self.freq.append(freq)

