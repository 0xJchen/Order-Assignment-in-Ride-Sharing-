import pickle
import greedy
import greedy2
import utility
import numpy as np
import matplotlib.pyplot as plt 

infile1_1 = open('violate1_1','rb')
infile1_2 = open('violate1_2','rb')
infile2_1 = open('violate2_1','rb')
infile2_2 = open('violate2_2','rb')
violate1_1 = pickle.load(infile1_1)
violate1_2 = pickle.load(infile1_2)
violate2_1 = pickle.load(infile2_1)
violate2_2 = pickle.load(infile2_2)

print('violate1_1:',violate1_1)
print('violate1_2:',violate1_2)
print('violate2_1:',violate2_1)
print('violate2_2:',violate2_2)
print('violate1_1_count:',sum(violate1_1[i]!=0 for i in range(len(violate1_1))))
print('violate1_2_count:',sum(violate1_2[i]!=0 for i in range(len(violate1_2))))
print('violate2_1_count:',sum(violate2_1[i]!=0 for i in range(len(violate2_1))))
print('violate2_2_count:',sum(violate2_2[i]!=0 for i in range(len(violate2_2))))
