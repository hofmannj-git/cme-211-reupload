import sys
import time
import math


def loaddata(grades_file):
    """ This function takes in the argument "grades_file" for the desired \
        input file to read, and outputs the data in the desired formats. \n
        'studentid_list' - a list of the student IDs in the input file \n
        'hwgrades_dict' - a dict with all student IDs (keys) and a list of hw \
            grades (values), in the order they were provided in input file \n
        'examgrades_dict' - a dict with all student IDs (keys) and a list of \
            exam grades (values) """

    with open(grades_file, 'r') as f:
        total_lines = f.readlines()
    
    studentid_list = []
    hwgrades_dict = dict()
    examgrades_dict = dict()

    count = 0
    for line in total_lines:
        templine = total_lines[count].split()
        studentid_list.append(templine[0])
        temp_hw = [float(x) for x in templine[1:-2]]
        temp_exam = [float(x) for x in templine[-2:]]
        hwgrades_dict[templine[0]] = temp_hw
        examgrades_dict[templine[0]] = temp_exam
        count += 1
    
    return studentid_list, hwgrades_dict, examgrades_dict


def outputdata(studentid_list, lowest_index_dict, avg_grade_dict, output_file):
    """ This function takes in the arguments for the student id list, the \
        index with the lowest homework score, and the final grade, and writes \
        to file in the desired format as tup_list. \n"""

    tup_list = []
    for i in studentid_list:
        tup_list.append((i, lowest_index_dict[i], avg_grade_dict[i]))
    tup_list.sort(key = lambda x : x[2], reverse = True)

    with open(output_file, 'w') as g:
        for j in tup_list:
            g.write("{} {} {:0.3f}\n".format(j[0], j[1], j[2]))


def lowest_hw(m_avg_input):
    """ This function determines the lowest homework score for a student with \
        the input 'id' and outputs it. \n
        'lowest_hw_num' = the lowest hw score (for m) for that student """
    
    lowest_hw_num = min(m_avg_input)

    return lowest_hw_num


def calc_assignment(m_input, k_input, w_floats, hwgrades_dict_id):
    """ This function determines the aggregated assignment score for the \
        student with 'id' given the inputted 'k' and weights 'w', and calls \
        the next function to find the lowest hw score"""
    
    m_avg = []
    m_sum = 0
    for m in range(0,m_input): # for each m
        for k in range(0,k_input): # for each k
            m_sum += hwgrades_dict_id[ k_input*m + k ] * w_floats[k]
        m_avg.append(m_sum)
    
    return m_avg


def calc_avg(m_avg):
    """ This function determines the average assignment score, after the \
        lowest score has been dropped, and returns the average hw score. \n
        'assignment_num' = the average hw score for that student """
    
    assignment_num = 0
    for i in range(0,len(m_avg)):
        assignment_num += m_avg[i]
    
    assignment_num = assignment_num/len(m_avg)
    
    return assignment_num



# BODY OF CODE

if __name__ == "__main__": # reads command line
    
    if len(sys.argv) <= 4:
        print("Usage:")
        print("  $ python3 gradebook.py <grades_file> <output_file> <m> <k> " \
              "[w_1 w_2 ... w_k (default 1/k)]")
        sys.exit(0)
              
    # declares variables from inputs
    grades_file = sys.argv[1]
    output_file = sys.argv[2]
    m_input = int(sys.argv[3]) # always > 1
    k_input = int(sys.argv[4]) # always > 1

    if len(sys.argv) > 5:
        w_input = (sys.argv[5]).split() # real numbers
        w_floats = [float(x) for x in w_input] # convert to floats
        tot_w = 0 # for the total summing to one
        bool_w = True
        for j in range(0,len(w_input)):
            tot_w += w_floats[j]
            if not 0 <= w_floats[j] <= 1:
                bool_w = False
        # GENERATE EXCEPTION: requirements of weights
        if not bool_w and not math.isclose(1,tot_w):
            raise RuntimeError("The weights should sum to one and lie in the " \
                               "interval between 0 and 1.")
    else:
        w_floats = []
        for i in range(1,k_input+1):
            w_floats.append(1/float(k_input))

    inittime = time.time()

    # loads data and unpacks tuple output
    studentid_list, hwgrades_dict, examgrades_dict = loaddata(grades_file)

    lowest_index_dict = dict()
    avg_grade_dict = dict()
    for id in studentid_list:
        m_avg = calc_assignment(m_input, k_input, w_floats, \
                                         hwgrades_dict[id])
        lowest_hw_num = lowest_hw(m_avg)
        # removes first item from list where value is lowest hw grade
        lowest_index_dict[id] = m_avg.index(lowest_hw_num)
        m_avg.remove(lowest_hw_num)
        assignment_num = calc_avg(m_avg)
        avg_grade_dict[id] = assignment_num*0.5 + 0.25* \
                    (examgrades_dict[id][0]) + 0.25*(examgrades_dict[id][1])

    outputdata(studentid_list, lowest_index_dict, avg_grade_dict, output_file)


    finaltime = time.time()
    timeelapsed = finaltime - inittime
    print(timeelapsed)
