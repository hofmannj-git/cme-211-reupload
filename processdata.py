import sys
import time
import random

if __name__ == "__main__": # Reads the command line inputs
    # if no arguments, prints usage message
    
    if len(sys.argv) <= 2:
        print("Usage:")
        print("  $ python3 processdata.py <reference_file> <reads_file> \ <align_file>")
        sys.exit(0)
    
    # declares files names from input arguments
    reference_file = sys.argv[1]
    reads_file = sys.argv[2]
    align_file = sys.argv[3]

    # reads in the data from the reference and reads files specified
    with open(reference_file, 'r') as f:
        reference_whole = f.readline()
    count = 0
    with open(reads_file, 'r') as f:
        reads_preformat = f.readlines()
        reads_all = [0]*len(reads_preformat)
        for linenum in reads_preformat:
            # ensures only getting the read, not /n
            reads_all[count] = str(reads_preformat[count])
            count += 1

# ALIGNING THE DATA

inittime = time.time()

# initializes counts for number of alignments and reads list
count_zero = 0
count_one = 0
count_two = 0
align_all = [0]*len(reads_all)

for i in range(len(reads_all)):
    string2find = str(reads_all[i][:-1])
    iffound = reference_whole.find(string2find)
    # adds first alignment value to reads
    align_all[i] = "{0} {1}" .format(string2find, iffound)
    
    # if an alignment was found, continue to look for other alignments
    if iffound != -1:
        # check the rest of the reference AFTER the already found match
        iffound2 = reference_whole.find(string2find, (iffound + 1))
        if iffound2 != -1:
            align_all[i] = "{0} {1}" .format(align_all[i], iffound2)
            count_two += 1
        else:
            count_one += 1
    else:
        count_zero += 1

finaltime = time.time()
timeelapsed = finaltime - inittime

# prints desired outputs for command line
print("reference length: {}".format(len(reference_whole[:-1])))
print("number reads: {}".format(len(reads_all)))
print("read length: {}".format(len(reads_all[0][:-1])))
print("aligns 0: {}".format(count_zero/len(reads_all)))
print("aligns 1: {}".format(count_one/len(reads_all)))
print("aligns 2: {}".format(count_two/len(reads_all)))
print("elapsed time: {}".format(timeelapsed))

# writes the datasets to disk based on file name input in command line
with open(align_file, 'w') as g:
    for m in range(len(reads_all)): # cycles through reads to write per line
        g.write("{}\n".format(align_all[m]))
