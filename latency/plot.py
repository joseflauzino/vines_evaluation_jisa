#!/usr/bin/python
# coding=utf-8
import sys
import matplotlib
import matplotlib.pyplot as plot
from matplotlib import colors as mcolors
import numpy as np

matplotlib.rcParams.update({'font.size': 18})
matplotlib.rc('axes', labelsize=24)

x_range = 5000
labels = ['2 VNFs','3 VNFs','4 VNFs', '5 VNFs']
def make_plot(n, data, limit, step):
	x = np.arange(0,x_range,step)
	fig, axes = plot.subplots()
	fig.subplots_adjust(left=0.15, bottom=0.15, right=0.99, top=1, wspace=0, hspace=0)
	axes.grid(True,linestyle='--',axis='y')
	i = 0
	for item in data:
		axes.bar(x, item, label=labels[i], width=step)
		i+=1
	axes.set_xlabel("Latency ("+u"\u03bcs"+")")
	axes.set_ylabel("Number of packets")
	axes.legend(loc='upper right')
	plot.savefig("plot/latency-cloudstack-%s.pdf" % n)

def round_int(x,step):
    #return 10 * ((x + 5) // 10)
    return step * (x // step)

def count_packets(raw_data, step):
	data = []
	x = np.arange(0,x_range,step) # X axis labels
	for i in range(len(x)):
		data.append(0)
	for j in raw_data:
		j=int(float(j)*1000) # convert ms to us
		j=round_int(j,step)
		if j >=0 and j < x_range:
			g_index = get_index(x,j)
			try:
				data[g_index]+=1
			except:
				print("Exception: trying to increment o index %s. Value=%s" % (g_index,j))
	return data

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def get_index(arr,i):
	index=0
	for item in arr:
		if item == i:
			break
		index+=1
	return index

def main(n, qtd_vnfs, limit, step):
	data = []
	for i_qtd_vnfs in range(2,qtd_vnfs+1):
		current_file = "output/%sx/cloudstack-%svnfs.txt" % (n,i_qtd_vnfs)
		with open(current_file) as raw_data:
			data.append(count_packets(raw_data, step))
	make_plot(n, data, limit, step)
	print("Done")

if __name__ == "__main__":
	msg = """
	Incorrect usage.
	The correct mode is: python plot.py <n> <qtd_vnfs> <limit> <step>
	Where:
	n        number of times that the latency test was executed
	qtd_vnfs max number of VNFs
	limit    limit of values (index) to read from files
	step     the spacing (difference) between each two consecutive values in x axis
	"""
	if len(sys.argv) != 5:
		sys.exit(msg)
	main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))