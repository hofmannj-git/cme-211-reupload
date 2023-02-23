import math
import numpy as np
from scipy.interpolate import interp1d
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def loaddata(inputfile, solnfile):
    """ This function takes in the inputs 'solnfile' and 'inputfile' and reads \
        & loads the data from those files."""
    with open(inputfile, "r") as f:
        count = 0
        for line in f:
            if count == 0:
                len = float(line.split()[0])
                wid = float(line.split()[1])
                h = float(line.split()[2])
                count += 1
            else:
                Tc = float(line.split()[0])
                Th = float(line.split()[1])
    soln = np.loadtxt(solnfile, dtype=np.float)
    return len, wid, h, Tc, Th, soln


def addboundaries(soln, len, wid, h, Tc, Th):
    """ This function takes in the numpy array with the solution data and adds \
        the boundaries given the other parameters."""
    
    num_rows = int(wid/h);
    num_col = int(len/h);
    
    # adding left-most column
    full_soln = np.array([Th])
    for i in range(0,num_rows-2):
        full_soln = np.append(full_soln, soln[(num_col-2)*(num_rows-2)+i])
    full_soln = np.append(full_soln, [-Tc*(math.exp(-10.0*(-len/2)**2.0)-2.0)])
    full_soln = np.expand_dims(full_soln, axis=1)
    full_soln = np.flipud(full_soln)
    
    # adding remaining top and bottom positions
    for j in range(0,num_col-1):
        full_soln_i = np.array([Th])
        full_soln_i = np.append(full_soln_i, soln[j*(num_rows-2):((j+1)*(num_rows-2))])
        full_soln_i = np.append(full_soln_i, [-Tc*(math.exp(-10*(j*h+h-len/2)**2)-2)])
        full_soln_i = np.expand_dims(full_soln_i, axis=1)
        full_soln_i = np.flipud(full_soln_i)
        full_soln = np.concatenate((full_soln, full_soln_i),axis=1)

    return full_soln


def calcmeantemp(full_soln):
    """ This function calculates the average of the entire field."""
    
    sum = 0
    for k in range(0,full_soln.shape[0]):
        for l in range(0,full_soln.shape[1]):
            sum += full_soln[k][l]
    meantemp = sum/full_soln.size
    
    return meantemp


def calcisocline(full_soln, meantemp):
    """ This function calculates the row index for each column closest to the \
        mean temperature."""
    
    a = np.squeeze(np.full((full_soln.shape[0],1),meantemp))
    for i in range(0,full_soln.shape[1]):
        if i == 0:
            temp = np.abs(full_soln[:,i]-a)
            temp_1 = np.where(temp == temp.min())
            isocline = np.array([temp_1[0]])
        else:
            temp = np.abs(full_soln[:,i]-a)
            temp_1 = np.where(temp == temp.min())
            isocline = np.append(isocline, [temp_1[0]])

#print(isocline)
    
    return isocline


# BODY OF CODE

if __name__ == "__main__":
    
    # Determine if appropriate command line arguments were provided and if
    # not provide a usage message and exit.
    if len(sys.argv) != 3:
        print("Usage:")
        print("  $ python3 postprocess.py <input#.txt> <solution#.txt>")
        sys.exit(0)
    
    # declares variables from inputs
    inputfile = sys.argv[1]
    solnfile = sys.argv[2]

    # Store the solution in appropriate NumPy arrays
    len, wid, h, Tc, Th, soln = loaddata(inputfile, solnfile)
    # Adds the boundaries to the full solution
    full_soln = addboundaries(soln, len, wid, h, Tc, Th)

    # calculates the mean temperature & plots
    meantemp = calcmeantemp(full_soln)
    isocline = calcisocline(full_soln, meantemp)
    y, x = np.mgrid[slice(0, wid+h, h), slice(0, len+h, h)]
    fig, ax = plt.subplots()
    im = ax.pcolormesh(x, y, full_soln)
    fig.colorbar(im, ax=ax)

    x_n = np.linspace(0, len, num=len/h, endpoint=True)
    y_n = h*isocline
    func_plot = interp1d(x_n, y_n)
    xnew = np.linspace(0, len, num=len/h*100, endpoint=True)
    im1 = plt.plot(xnew, func_plot(xnew), 'k')

    # plt.axis([0.0, len, 0.0, wid])
    ax.set_xlabel("Y")
    ax.set_ylabel("X")
    plt.savefig("plot{}.png".format(inputfile[-5:-4]))

    print("Input file processed: " + inputfile)
    print("Mean Temperature: {:9.5f}".format(meantemp))
