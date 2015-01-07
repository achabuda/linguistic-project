#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function, division

CSV_DELIMITER = '\t'
WORD_SEPARATOR = '^'
CODING = 'utf-8'
WORD_SEPARATOR = '^'
FORBIDDEN_CHARACTERS = set('1234567890')

BRILLE_LETTERS = set(u'ąbciek')
VOLVES = set(u'iyeaoóuąę')
TRESHOLD_LETTERS = u'k' # freq letters=>freq k, freq letters=<freq k
PERCENTAGLE_UPPER = 70
PERCENTAGLE_LOWER = 40
TARGET_POSITION = [2,3,4]
