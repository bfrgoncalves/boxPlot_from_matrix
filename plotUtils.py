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


def importData_Matrix(filename):
    #start_time = time.time()
    matrix=[]
    row_header=[]
    first_row=True

    if '/' in filename:
        dataset_name = string.split(filename,'/')[-1][:-4]
    else:
        dataset_name = string.split(filename,'\\')[-1][:-4]

        
    for line in open(filename,'rU').xreadlines():         
        t = string.split(line[:-1],'\t') ### remove end-of-line character - file is tab-delimited
        if first_row:
            column_header = t[1:]
            first_row=False
        else:
            if ' ' not in t and '' not in t: ### Occurs for rows with missing data
                s = map(float,t[1:])
                if (abs(max(s)-min(s)))>0:
                    matrix.append(s)
                    row_header.append(t[0])

    return matrix, column_header, row_header


def filter_by_indentifier(matrix, lineIdentifier, columnIndentifier):


    headers = matrix[1]
    countLines = 0
    allLineArray = []
    lineArray = []
    new_headersLine = []
    new_headersColumn = []
    firstTime = True

    for i in matrix[0]:
        if lineIdentifier in headers[countLines]:
            new_headersLine.append(headers[countLines])
            for j in range(0, len(headers)):
                if firstTime:
                    new_headersColumn.append(headers[j])
                if columnIndentifier in headers[j]:
                    lineArray.append(i[j])
            firstTime = False
            allLineArray.append(lineArray)
            lineArray = []
        countLines += 1

    new_matrix = (allLineArray, new_headersLine, new_headersColumn)

    print new_matrix

    return new_matrix
