#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import pandas as pd
import numpy as np
from itertools import permutations

'''
	Conditions:
	
		(1) strings of infrequent letters forming rare bigrams
		(2) strings of frequent letters forming rare bigrams
		(3) strings of frequent letters forming middle-frequency bigrams
	 	(4) strings of frequent letters forming frequent bigrams but rare quadrigrams
		(5) pseudowords (frequent letters forming frequent bigrams forming frequent quadrigrams)
'''

def get_ngrams_csv(file_name, d):
	df = pd.read_csv(file_name, delimiter=d)
	ngrams = [i for i in df['ngram']]
	freq = [i for i in df['freq']]
	return ngrams,freq

def get_letters(csv_file):
	df = pd.read_csv(csv_file, delimiter=',')
	grams = [i for i in df['gram']]
	idx = grams.index('k')
	return grams[:idx+1], grams[idx:]

def get_start_stop_ngrams(f_name):
	ngrams,freq = get_ngrams_csv(f_name,'\t') 
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

def get_ngrams(f_name):
	ngrams,freq = get_ngrams_csv(f_name,'\t')
	wrong_ids = [i for i,x in enumerate(ngrams) if '^' in str(x)]
	# ngrams = [item for i,item in enumerate(ngrams) if i not in t]	### much slower solution
	# freq = [item for i,item in enumerate(freq) if i not in t]
	wrong_ids = sorted(wrong_ids,reverse=True)
	for index in wrong_ids:
		del ngrams[index]
		del freq[index]
	return zip(ngrams,freq)

def write_to_csv(f_name,ngrams,start_ngrams,stop_ngrams):
	ngrams += start_ngrams
	ngrams += stop_ngrams 
	ngrams.sort(key=lambda x: x[1],reverse=True)
	print(ngrams[:100])
	df = pd.DataFrame({'ngrams': [x[0] for x in ngrams],
					   'freq': [x[1] for x in ngrams]})
	df.to_csv(f_name,sep=',')

def get_freqs_ngrams(ngrams,start_ngrams,stop_ngrams,upper,lower):
	ngrams += start_ngrams
	ngrams += stop_ngrams 
	ngrams.sort(key=lambda x: x[1],reverse=True)
	freq = [x[1] for x in ngrams]
	ngrams = [x[0] for x in ngrams]
	per_lower = np.percentile(freq,lower)
	per_upper = np.percentile(freq,upper)
	ind_lower = min(freq, key=lambda x:abs(x-per_lower)) ## finds maximal index
	ind_lower = max([i for i,x in enumerate(freq) if x == ind_lower])
	ind_upper = freq.index(min(freq, key=lambda x:abs(x-per_upper)))
	# ind_20 = max([i for i,x in enumerate(freq) if x == per_lower])
	# ind_30 = min([i for i,x in enumerate(freq) if x == per_upper])
	mf_ngrams = ngrams[ind_upper:ind_lower+1]
	lf_ngrams = ngrams[ind_lower:]
	# per_80 = int(np.percentile(freq,upper))
	# ind_80 = freq.index(min(freq, key=lambda x:abs(x-per_80)))
	hf_ngrams = ngrams[:ind_upper+1]
	return lf_ngrams,mf_ngrams,hf_ngrams

def compute_sequences(bigrams,freq_letters,vowels,two_braille):
	'''
		- 60 ciągów zawierających jedną literę 2-kropkową na pozycji 2,3 lub 4 
		  (wariant z jedną samogłoską)
		- 60 ciągów zawierających jedną literę 2-kropkową na pozycji 2,3 lub 4 
		  (wariant bez samogłoski)
		- 60 ciągów NIE zawierających żadnej litery 2-kropkowej
		  (wariant z jedną samogłoską)
		- 60 ciągów NIE zawierających żadnej litery 2-kropkowej
		  (wariant bez samogłoski)
	'''
	x = []
	for b in bigrams:
		if len(str(b)) == 2:
			if str(b[0]) in freq_letters and str(b[1]) in freq_letters:
				x.append(b)
		elif len(str(b)) == 3 and str(b[0]) == '^':
			if str(b[1]) in freq_letters and str(b[2]) in freq_letters:
				x.append(b)
		elif len(str(b)) == 3 and str(b[2]) == '^':
			if str(b[0]) in freq_letters and str(b[1]) in freq_letters:
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
		if len(two_braille & set(p)) == 1 and len(vowels & set(p)) == 1:
			seq_1 = _append_to_sequence(seq_1,p,two_braille)
		elif len(two_braille & set(p)) == 1 and len(vowels & set(p)) == 0:
			seq_2 = _append_to_sequence(seq_2,p,two_braille)
		elif len(two_braille & set(p)) == 0 and len(vowels & set(p)) == 1:
			seq_3.append(p)
		elif len(two_braille & set(p)) == 0 and len(vowels & set(p)) == 0:
			seq_4.append(p)
	return seq_1,seq_2,seq_3,seq_4

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

def sequence_with_quadrigrams(bigrams,freq_letters,vowels,two_braille,freq_quadrigrams):
	seq_1_temp,seq_2_temp,seq_3_temp,seq_4_temp = compute_sequences(bigrams,freq_letters,vowels,two_braille)
	seq_1 = [i for i in seq_1_temp if i in freq_quadrigrams]
	seq_2 = [i for i in seq_2_temp if i in freq_quadrigrams]
	seq_3 = [i for i in seq_3_temp if i in freq_quadrigrams]
	seq_4 = [i for i in seq_4_temp if i in freq_quadrigrams]
	return seq_1,seq_2,seq_3,seq_4

def write_result(condition,seq1,seq2,seq3,seq4):
	out_file = './result_'+condition+'.csv'
	df = pd.DataFrame({'variant1': seq1,
					   'variant2': seq2,
					   'variant3': seq3,
					   'variant4': seq4})
	df.to_csv(out_file,sep=',',encoding='utf-8')

if __name__ == '__main__':

	two_braille = set('ąbciek')
	vowels = set('iyeaoóuąę')
	freq_letters,infreq_letters = get_letters('./lista liter w alfabecie polskim wraz z iloscia kropek brajl.csv')

	bigrams = get_ngrams('./data/bigrams.csv')
	start_bigrams,stop_bigrams = get_start_stop_ngrams('./data/trigrams.csv')
	# write_to_csv('./all_bigrams.csv',bigrams,start_bigrams,stop_bigrams)
	lf_bigrams,mf_bigrams,hf_bigrams = get_freqs_ngrams(bigrams,start_bigrams,stop_bigrams,upper=50,lower=30)

	# seq_1,seq_2,seq_3,seq_4 = compute_sequences(lf_bigrams,infreq_letters,vowels,two_braille)	### condition 1, lower=45
	# print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	# write_result('lf_bigrams_infreq',seq_1[:60],seq_2[:60],seq_3[:60],seq_4[:60])

	# seq_1,seq_2,seq_3,seq_4 = compute_sequences(lf_bigrams,freq_letters,vowels,two_braille)	### condition 2, lower=48
	# print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	# write_result('lf_bigrams_freq',seq_1[:60],seq_2[:60],seq_3[:60],seq_4[:60])

	# seq_1,seq_2,seq_3,seq_4 = compute_sequences(mf_bigrams,freq_letters,vowels,two_braille)	### condition 3, upper=50, lower=30
	# print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	# write_result('mf_bigrams_freq',seq_1[:60],seq_2[:60],seq_3[:60],seq_4[:60])

	quadrigrams = get_ngrams('./data/quadrigrams.csv')
	start_quadrigrams,stop_quadrigrams = get_start_stop_ngrams('./data/pentagrams.csv')
	# # write_to_csv('./all_quadrigrams.csv',quadrigrams,start_quadrigrams,stop_quadrigrams)

	lf_quadrigrams,mf_quadrigrams,hf_quadrigrams = get_freqs_ngrams(quadrigrams,start_quadrigrams,stop_quadrigrams,upper=50,lower=50)

	seq_1,seq_2,seq_3,seq_4 = sequence_with_quadrigrams(hf_bigrams,freq_letters,vowels,two_braille,lf_quadrigrams)	### condition 4
	print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	# write_result('hf_bigrams_freq_lf_quadr',seq_1[:60],seq_2[:60],seq_3[:60],seq_4[:60])

	# seq_1,seq_2,seq_3,seq_4 = sequence_with_quadrigrams(hf_bigrams,freq_letters,vowels,two_braille,hf_quadrigrams)	### condition 5
	# print(len(seq_1),len(seq_2),len(seq_3),len(seq_4))
	# write_result('hf_bigrams_freq_hf_quadr',seq_1[:60],seq_2[:60],seq_3[:60],seq_4[:60])

	# words = csv_reader('./subtlex-pl_filtrowany.csv',',')
