import random
import sys
import time

inittime = time.time()

if __name__ == "__main__": # Reads the command line inputs
    # if no arguments, prints usage message
    
    if len(sys.argv) <= 5:
        print("Usage:")
        print("  $ python3 generatedata.py <ref_length> <nreads> <read_len> \
              <ref_file> <reads_file>")
        sys.exit(0)
    
    # declares parameters from input arguments
    ref_length = int(sys.argv[1])
    nreads = int(sys.argv[2])
    read_len = int(sys.argv[3])
    ref_file = sys.argv[4]
    reads_file = sys.argv[5]

# CREATING THE REFERENCE SEQUENCE

reference_temp = '0'   # Establishes variable
ref_rand_length = int(0.75*ref_length)
ref_quarter_length = int(0.25*ref_length)
# loops through each position to the desired length of 75% of the reference
for i in range(ref_rand_length):
    
    temp_num = random.randint(0,3)
    # assigns the random four numbers to letters
    if temp_num == 0:
        temp_letter = "A"
    elif temp_num == 1:
        temp_letter = "C"
    elif temp_num == 2:
        temp_letter = "G"
    elif temp_num == 3:
        temp_letter = "T"
    
    # concatenates the random letters together
    if i == 0:
        reference_temp = temp_letter
    else:
        reference_temp += temp_letter

# duplicates the last 25% and adds to the end
reference_quarter = reference_temp[-ref_quarter_length:]
reference_whole = reference_temp + reference_quarter


# CREATING THE READS

# initializes counts for number of alignments and reads list
count_zero = 0
count_one = 0
count_two = 0
reads_all = [0]*nreads

# loops through each desired read
for j in range(nreads):
    
    temp_align = random.random()
    
    if temp_align <= 0.15:  # Generates reads with no alignments
        while True:
            for k in range(read_len):
                
                # randomly picks between 4 numbers
                temp_num = random.randint(0,3)
                # assigns the random four numbers to letters
                if temp_num == 0:
                    temp_letter = "A"
                elif temp_num == 1:
                    temp_letter = "C"
                elif temp_num == 2:
                    temp_letter = "G"
                elif temp_num == 3:
                    temp_letter = "T"
                        
                # concatenates the random letters together
                if k == 0:
                    read_temp = temp_letter
                else:
                    read_temp += temp_letter
                        
            if reference_whole.find(read_temp) == -1:
                reads_all[j] = read_temp
                break
                    
        count_zero += 1
    
    elif 0.15 < temp_align <= 0.90: # Generates reads with one alignment
        start_pos = random.randint(0,ref_length/2)
        # Assigns values to read list based on random start pos. & read length
        reads_all[j] = reference_whole[start_pos:(start_pos + read_len)]
        count_one += 1
    
    elif temp_align > 0.90: # Generates reads with two alignments
        start_pos = random.randint(ref_length/2, (ref_length - read_len))
        # Assigns values to read list based on random start pos. & read length
        reads_all[j] = reference_whole[start_pos:(start_pos + read_len)]
        count_two += 1

finaltime = time.time()
timeelapsed = finaltime - inittime

# prints desired outputs for command line
print("reference length: {}".format(len(reference_whole)))
print("number reads: {}".format(len(reads_all)))
print("read length: {}".format(len(reads_all[0])))
print("aligns 0: {}".format(count_zero/nreads))
print("aligns 1: {}".format(count_one/nreads))
print("aligns 2: {}".format(count_two/nreads))
# print("elapsed time: {}".format(timeelapsed))

# writes the datasets to disk based on file names input in command line
with open(ref_file, 'w') as f:
    f.write("{}\n".format(reference_whole))
with open(reads_file, 'w') as g:
    for m in range(nreads): # cycles through each read to write per line
        g.write("{}\n".format(reads_all[m]))
