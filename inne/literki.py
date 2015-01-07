#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import pandas as pd
import numpy as np
from itertools import permutations

#****************************************************************************************
'''read data from bigrams,...'''

def read_from_csv_data(bigrams, trigrams, quadrigrams, pentagrams, words):
	bigrams = _get_ngrams('./data/bigrams.csv')
	start_bigrams, stop_bigrams = _get_start_stop_ngrams('./data/trigrams.csv')
	bigrams = _filter_ngrams(bigrams)
	start_bigrams = _filter_ngrams(start_bigrams)
	stop_bigrams = _filter_ngrams(stop_bigrams)

	quadrigrams = _get_ngrams('./data/quadrigrams.csv')
	start_quadrigrams,stop_quadrigrams = _get_start_stop_ngrams('./data/pentagrams.csv')
	quadrigrams = _filter_ngrams(quadrigrams)
	start_quadrigrams = _filter_ngrams(start_quadrigrams)
	stop_quadrigrams = _filter_ngrams(stop_quadrigrams)

	words = get_words(words)
	return bigrams, start_bigrams, stop_bigrams, quadrigrams, start_quadrigrams, stop_quadrigrams, words

def _get_ngrams(f_name):
	df = pd.read_csv(f_name, delimiter='\t')
	ngrams = [i for i in df['ngram']]
	freq = [i for i in df['freq']]
	wrong_ids = [i for i,x in enumerate(ngrams) if '^' in str(x)]
	wrong_ids = sorted(wrong_ids,reverse=True)
	for index in wrong_ids:
		del ngrams[index]
		del freq[index]
	return zip(ngrams, freq)

def _get_start_stop_ngrams(f_name):
	df = pd.read_csv(f_name, delimiter='\t')
	ngrams = [i for i in df['ngram']]
	freq = [i for i in df['freq']]
	t = [i for i,x in enumerate(ngrams) if '^^' in str(x)]
	tt =[i for i,x in enumerate(ngrams) if '^' == str(x)[0] and '^' == str(x)[-1]]
	t += tt
	ngrams = [item for i,item in enumerate(ngrams) if i not in t]
	freq = [item for i,item in enumerate(freq) if i not in t]
	start_ngrams = []
	stop_ngrams = []
	for i,t in enumerate(ngrams):
		if str(t)[0] == '^':
			start_ngrams.append((t,freq[i]))
		if str(t)[-1] == '^':
			stop_ngrams.append((t,freq[i]))
	return start_ngrams, stop_ngrams

def _filter_ngrams(ngrams):
	ngrams.sort(key=lambda x: x[1],reverse=True)
	non_num_ngrams = [(n.decode('utf-8'),f) for n, f in ngrams if len(set('1234567890') & set(n)) == 0]
	return non_num_ngrams

def get_words(f_name):
	df = pd.read_csv(f_name, ',')
	all_words = [i.decode('utf-8') for i in df['Word']]
	all_freq = [i for i in df['FreqSum']]
	all_len = [i for i in df['dlugosc']]
	word = [(w, all_freq[i])  for i, w in enumerate(all_words) if all_len[i]==4]
	return word

def write_to_csv(f_name,ngrams):
	ngrams.sort(key=lambda x: x[1],reverse=True)
	df = pd.DataFrame({'ngrams': [x[0] for x in ngrams],'freq': [x[1] for x in ngrams]})
	df.to_csv(f_name,sep=',')

def get_letters(csv_file):
	df = pd.read_csv(csv_file, delimiter=',')
	grams = [i.decode('utf-8') for i in df['gram']]
	idx = grams.index('k')
	return grams[:idx+1], grams[idx:]  #freq_letters, infreq_letters
#*******************************************************************************************

#*******************************************************************************************
'''
	Conditions:
	
		(1) strings of infrequent letters forming rare bigrams
		(2) strings of frequent letters forming rare bigrams
		(3) strings of frequent letters forming middle-frequency bigrams
		(4) strings of frequent letters forming frequent bigrams but rare quadrigrams
		(5) pseudowords (frequent letters forming frequent bigrams forming frequent quadrigrams)
		(6) words


	for each condition:
		seq1 - 60 ciągów zawierających jedną literę 2-kropkową na pozycji 2,3 lub 4 
		  (wariant z jedną samogłoską)
		seq2 - 60 ciągów zawierających jedną literę 2-kropkową na pozycji 2,3 lub 4 
		  (wariant bez samogłoski)
		seq3 - 60 ciągów NIE zawierających żadnej litery 2-kropkowej
		  (wariant z jedną samogłoską)
		seq4 - 60 ciągów NIE zawierających żadnej litery 2-kropkowej
		  (wariant bez samogłoski)
'''

def _append_to_sequence(seq,p,two_braille):
	try:
		v = list(two_braille & set(p))[0]
		if len(p) == 4 and p.index(v) in (1,2,3):
			seq.append(p)
		if len(p) in (5,6) and p.startswith('^') and p.index(v) in (2,3,4):
			seq.append(p)
		if len(p) == 5 and p.endswith('^') and p.index(v) in (1,2,3):
			seq.append(p)
	except IndexError:
		pass
	return seq

def get_freqs_ngrams(ngrams,upper=50,lower=20):
	ngrams.sort(key=lambda x: x[1],reverse=True)
	freq = [x[1] for x in ngrams]
	ngrams = [x[0] for x in ngrams]
	per_lower = np.percentile(freq,lower)
	per_upper = np.percentile(freq,upper)
	ind_lower = min(freq, key=lambda x:abs(x-per_lower)) ## finds maximal index
	ind_lower = max([i for i,x in enumerate(freq) if x == ind_lower])
	ind_upper = freq.index(min(freq, key=lambda x:abs(x-per_upper)))
	mf_ngrams = ngrams[ind_upper:ind_lower+1]
	lf_ngrams = ngrams[ind_lower:]
	per_80 = int(np.percentile(freq,upper))
	ind_80 = freq.index(min(freq, key=lambda x:abs(x-per_80)))
	hf_ngrams = ngrams[:ind_80+1]
	return lf_ngrams,mf_ngrams,hf_ngrams
#*****************************************************************


def compute_sequences(bigrams, all_ngrams,freq_letters,vowels,two_braille):
	x = []
	for b in all_ngrams:
		if len(b) == 2:
			if b[0] in freq_letters and b[1] in freq_letters:
				x.append(b)
		elif len(b) == 3 and b[0] == '^':
			if b[1] in freq_letters and b[2] in freq_letters:
				x.append(b)
		elif len(b) == 3 and b[2] == '^':
			if b[0] in freq_letters and b[1] in freq_letters:
				x.append(b)
	perms = [''.join(p) for p in permutations(x,2)]
	wrong_ids = []
	for i,p in enumerate(perms):
		if p.count('^') > 0 and not p.startswith('^') and not p.endswith('^'):
			wrong_ids.append(i)
		elif p.count('^') == 2 and p.startswith('^') and not p.endswith('^'):
			wrong_ids.append(i)
		elif p.count('^') == 2 and p.endswith('^') and not p.startswith('^'):
			wrong_ids.append(i)
		elif p.count('^') == 3 and p.endswith('^') and p.startswith('^'):
			wrong_ids.append(i)
	wrong_ids = sorted(wrong_ids,reverse=True)
	for index in wrong_ids:
		del perms[index]
	seq_1 = []
	seq_2 = []
	seq_3 = []
	seq_4 = []
	for p in perms:
		if len(two_braille & set(p)) == 1 and len(vowels & set(p)) == 1: #
			seq_1 = _append_to_sequence(seq_1,p,two_braille)
		elif len(two_braille & set(p)) == 1 and len(vowels & set(p)) == 0:
			seq_2 = _append_to_sequence(seq_2,p,two_braille)
		elif len(two_braille & set(p)) == 0 and len(vowels & set(p)) == 1:
			seq_3.append(p)
		elif len(two_braille & set(p)) == 0 and len(vowels & set(p)) == 0:
			seq_4.append(p)
	seq_1 = [s.strip('^') for s in seq_1 if s[2:4] in set(bigrams)]
	seq_2 = [s.strip('^') for s in seq_2 if s[2:4] in set(bigrams)]
	seq_3 = [s.strip('^') for s in seq_3 if s[2:4] in set(bigrams)]
	seq_4 = [s.strip('^') for s in seq_4 if s[2:4] in set(bigrams)]
	return seq_1,seq_2,seq_3,seq_4

def sequence_with_bigrams(bigrams,start_bigrams,stop_bigrams,freq_letters,vowels,two_braille):		
	all_bigrams = start_bigrams+stop_bigrams
	return compute_sequences(bigrams, all_bigrams,freq_letters,vowels,two_braille)

def sequence_with_quadrigrams(bigrams, start_bigrams, stop_bigrams, freq_letters,vowels,two_braille,freq_quadrigrams,words):
	all_bigrams = start_bigrams+stop_bigrams
	seq_1_temp,seq_2_temp,seq_3_temp,seq_4_temp = compute_sequences(bigrams, all_bigrams, freq_letters,vowels,two_braille)
	words = [w for w,f in words]
	freq_quadrigrams = [i.strip('^') for i in freq_quadrigrams]
	seq_1 = [i.strip('^') for i in seq_1_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') not in words)]
	seq_2 = [i.strip('^') for i in seq_2_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') not in words)]
	seq_3 = [i.strip('^') for i in seq_3_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') not in words)]
	seq_4 = [i.strip('^') for i in seq_4_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') not in words)]
	return seq_1,seq_2,seq_3,seq_4

def sequence_with_words(bigrams, start_bigrams, stop_bigrams, freq_letters,vowels,two_braille,freq_quadrigrams,words):
	all_bigrams = start_bigrams+stop_bigrams
	seq_1_temp,seq_2_temp,seq_3_temp,seq_4_temp = compute_sequences(bigrams, all_bigrams, freq_letters,vowels,two_braille)
	words = [w for w,f in words]
	freq_quadrigrams = [i.strip('^') for i in freq_quadrigrams]
	seq_1 = [i.strip('^') for i in seq_1_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') in words)]
	seq_2 = [i.strip('^') for i in seq_2_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') in words)]
	seq_3 = [i.strip('^') for i in seq_3_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') in words)]
	seq_4 = [i.strip('^') for i in seq_4_temp if (i.strip('^') in freq_quadrigrams and i.strip('^') in words)]
	return seq_1,seq_2,seq_3,seq_4\

def word_with_freq_letters(letters, words):
	return [w[0] for w in words if len(set(w[0]) & set(letters))==4]

def write_result(condition,seq1,seq2,seq3,seq4):
	out_file = './result_'+condition+'.csv'
	max_ = max(len(seq1),len(seq2),len(seq3),len(seq4))
	seq1 = seq1+[0]*(max_-len(seq1))
	seq2 = seq2+[0]*(max_-len(seq2))
	seq3 = seq3+[0]*(max_-len(seq3))
	seq4 = seq4+[0]*(max_-len(seq4))
	df = pd.DataFrame({'variant1': seq1,
					   'variant2': seq2,
					   'variant3': seq3,
					   'variant4': seq4})
	df.to_csv(out_file,sep=',',encoding='utf-8')

if __name__ == '__main__':

	two_braille = set(u'ąbciek')
	vowels = set(u'iyeaoóuąę')
	freq_letters, infreq_letters = get_letters('./lista liter w alfabecie polskim wraz z iloscia kropek brajl.csv')
	try:
		bigrams = pd.read_csv('./csv_data/bigrams.csv', ',')
		start_bigrams = pd.read_csv('./csv_data/start_bigrams.csv', ',')
		stop_bigrams = pd.read_csv('./csv_data/stop_bigrams.csv', ',')
		quadrigrams = pd.read_csv('./csv_data/quadrigrams.csv', ',')
		start_quadrigrams = pd.read_csv('./csv_data/start_quadrigrams.csv', ',')
		stop_quadrigrams = pd.read_csv('./csv_data/stop_quadrigrams.csv', ',')
		words = pd.read_csv('./csv_data/words_four.csv', ',')

		bigrams = zip([i.decode('utf-8') for i in bigrams.ngrams], bigrams.freq)
		start_bigrams = zip([i.decode('utf-8') for i in start_bigrams.ngrams], start_bigrams.freq)
		stop_bigrams = zip([i.decode('utf-8') for i in stop_bigrams.ngrams], stop_bigrams.freq)
		quadrigrams = zip([i.decode('utf-8') for i in quadrigrams.ngrams], quadrigrams.freq)
		start_quadrigrams = zip([i.decode('utf-8') for i in start_quadrigrams.ngrams], start_quadrigrams.freq)
		stop_quadrigrams = zip([i.decode('utf-8') for i in stop_quadrigrams.ngrams], stop_quadrigrams.freq)
		words = zip([i.decode('utf-8') for i in words.ngrams], words.freq)

	except IOError:
		bigrams, start_bigrams, stop_bigrams, quadrigrams, start_quadrigrams, stop_quadrigrams, words = read_from_csv_data('./data/bigrams.csv', './data/trigrams.csv', './data/quadrigrams.csv', './data/pentagrams.csv', './data/korpus.csv')
		write_to_csv('./csv_data/bigrams.csv', bigrams)
		write_to_csv('./csv_data/start_bigrams.csv', start_bigrams)
		write_to_csv('./csv_data/stop_bigrams.csv', stop_bigrams)
		write_to_csv('./csv_data/quadrigrams.csv', quadrigrams)
		write_to_csv('./csv_data/start_quadrigrams.csv', start_quadrigrams)
		write_to_csv('./csv_data/stop_quadrigrams.csv', stop_quadrigrams)
		write_to_csv('./csv_data/words_four.csv', words)

	lf_bigrams,mf_bigrams,hf_bigrams = get_freqs_ngrams(bigrams,upper=70,lower=40)
	lf_bigrams_start,mf_bigrams_start,hf_bigrams_start = get_freqs_ngrams(start_bigrams,upper=70,lower=40)
	lf_bigrams_stop,mf_bigrams_stop,hf_bigrams_stop = get_freqs_ngrams(stop_bigrams,upper=70,lower=40)

	seq_1,seq_2,seq_3,seq_4 = sequence_with_bigrams(lf_bigrams, lf_bigrams_start, lf_bigrams_stop, infreq_letters,vowels,two_braille) ### condition 1
	print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	write_result('lf_bigrams_infreq',seq_1,seq_2,seq_3,seq_4)
	seq_1,seq_2,seq_3,seq_4 = sequence_with_bigrams(lf_bigrams,lf_bigrams_start, lf_bigrams_stop, freq_letters,vowels,two_braille) ### condition 2
	print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	write_result('lf_bigrams_freq',seq_1,seq_2,seq_3,seq_4)
	seq_1,seq_2,seq_3,seq_4 = sequence_with_bigrams(mf_bigrams,mf_bigrams_start,mf_bigrams_stop,freq_letters,vowels,two_braille) ### condition 3
	print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	write_result('nf_bigrams_freq',seq_1,seq_2,seq_3,seq_4)

	quadrigrams += start_quadrigrams+stop_quadrigrams
	lf_quadrigrams,mf_quadrigrams,hf_quadrigrams = get_freqs_ngrams(quadrigrams,upper=70,lower=40)
	seq_1,seq_2,seq_3,seq_4 = sequence_with_quadrigrams(hf_bigrams,hf_bigrams_start,hf_bigrams_stop,freq_letters,vowels,two_braille,lf_quadrigrams,words)  ### condition 4
	print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	write_result('hf_bigrams_freq_lf_quadrigrams',seq_1,seq_2,seq_3,seq_4)

	seq_1,seq_2,seq_3,seq_4 = sequence_with_quadrigrams(hf_bigrams, hf_bigrams_start,hf_bigrams_stop,freq_letters,vowels,two_braille,hf_quadrigrams,words)  ### condition 5
	print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	write_result('hf_bigrams_freq_hf_quadrigrams',seq_1,seq_2,seq_3,seq_4)

	seq_1,seq_2,seq_3,seq_4 = sequence_with_words(bigrams,hf_bigrams_start,hf_bigrams_stop,freq_letters,vowels,two_braille,hf_quadrigrams,words) ### condition 6
	print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	write_result('word',seq_1,seq_2,seq_3,seq_4)
	w = word_with_freq_letters(freq_letters, words)
	print (len(w))
