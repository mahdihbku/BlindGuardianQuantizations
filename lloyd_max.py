#!/usr/bin/env python2
import numpy as np
import pandas as pd

data = pd.read_csv('reps_floats.csv', header=None).as_matrix()

# GENERATE ALL QUANTIZATION INTERVALS
all_intervals = []

for j in range(128):
	col = data[:,j]
	col.sort()
	intervals = []
	for nbr_bits in range(1, 9):
		sub_interval = []
		for i in range(2**nbr_bits):
			sub_interval.append(col[i*len(col)/2**nbr_bits])
		sub_interval.append(col[len(col)-1])
		intervals.append(sub_interval)
	all_intervals.append(intervals)
pd.DataFrame(all_intervals).to_csv("all_intervals.csv", header=None, index=None)

# GENERATE REPS
for nbr_bits in range(8):
	print("Handling nbr_bits={}".format(nbr_bits+1))
	lloyd_quantized_reps = []
	for i in range(len(data)):
		lloyd_quantized_rep = []
		for j in range(128):
			k = 0
			while(data[i][j] > all_intervals[j][nbr_bits][k+1]):	# works but must be a better way!
				k += 1
			lloyd_quantized_rep.append(k)
		lloyd_quantized_reps.append(lloyd_quantized_rep)
	file_name = "lloyd_quantized_reps_"+str(nbr_bits+1)+"bits.csv"
	pd.DataFrame(lloyd_quantized_reps).to_csv(file_name, header=None, index=None)
