import subprocess
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from datetime import datetime
import numpy
import string
import matplotlib.pyplot as plt
from pylab import *
from datetime import datetime

from plotUtils import importData_Matrix
from plotUtils import filter_by_indentifier

def main():

	parser = argparse.ArgumentParser(description="This program constructs box plots based on subsets of data in a matrix")
	parser.add_argument('-x', nargs='?', type=str, help="matrix File", required=True)
	parser.add_argument('-i', nargs='?', type=str, help="identifiers (comma separated)", required=False)
	parser.add_argument('-ia', nargs='?', type=str, help="identifier new label (comma separated)", required=False)
	parser.add_argument('-t', nargs='?', type=str, help="plot title", required=False)


	args = parser.parse_args()

	createPlot(args)


def createPlot(args):
	matrix = importData_Matrix(args.x)
	if args.i:
		identifiers = args.i.split(',')

	else:
		identifiers = ['']

	if args.ia:
		newLabels = args.ia.split(',')

	else:
		newLabels = identifiers

	data = []
	to_data = []

	fig, ax1 = plt.subplots(figsize=(10,6))
	fig.canvas.set_window_title('S.dysgalactiae Boxplot')
	plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

	# Add a horizontal grid to the plot, but make it very light in color
	# so we can use it for reading data values but not be distracting
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
	              alpha=0.5)

	# Hide these grid behind plot objects
	ax1.set_axisbelow(True)
	ax1.set_title(args.t)
	ax1.set_xlabel('Groups')
	ax1.set_ylabel('ANI values')
	top = 1.00
	bottom = 0.96

	ax1.set_ylim(bottom, top)

	comparisons = []
	for i in range(0,len(identifiers)-1):
		for j in range(i, len(identifiers)):

			if len(identifiers) == len(newLabels):
				comparisons.append(str(newLabels[i]) + ' / ' + newLabels[j])
			else:
				comparisons.append(str(identifiers[i]) + ' / ' + identifiers[j])
			new_values = filter_by_indentifier(matrix, identifiers[i], identifiers[j])

			for j in new_values[0]:
				to_data = to_data + j
			
			data.append(to_data)
			to_data = []


		# Set the axes ranges and axes labels
		print i
	bp = plt.boxplot(data)

	plt.setp(bp['boxes'], color='black')
	plt.setp(bp['whiskers'], color='black')
	plt.setp(bp['fliers'], color='red', marker='+')

	xtickNames = plt.setp(ax1, xticklabels=comparisons)
	plt.setp(xtickNames, rotation=45, fontsize=8)

	resultFile = 'boxplot' + '_' + str(datetime.now())
	resultFile= resultFile.replace(' ', '')
	resultFile = resultFile.replace(':', '_')
	resultFile = resultFile.replace('.', '_', 1)

	resultFileName = resultFile + '.tif'

	plt.savefig(resultFileName, dpi=300)

	plt.show()


if __name__ == "__main__":
	main()