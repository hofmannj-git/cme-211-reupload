import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import math
import numpy as np
import os.path
import scipy.sparse.linalg
import scipy.sparse as sp
import sys
import warnings

class Truss:
    """ This Truss class contains the methods: \n
        '__init__' - initialization and loading of data from input files \n
        'PlotGeometry' - creating a plot of the truss geometry and saving to \
            the destination specified in the input \n
        '__calc_forces' - computing the beam forces for the truss of interest \n
        '__repr__' - formats and returns the desired output string as the \
            representation of an instance of the class 'Truss' \n """
    

    def __init__(self, file_joint, file_beams):
        """ This initialization method takes in the names for the joint and \
            beam files and loads the data in the desired format. """
    
        self.__joint = np.loadtxt(file_joint, dtype=np.float64)
        self.__beams = np.loadtxt(file_beams, dtype=np.int)
        self.__zerodisp = self.__joint[:,5].astype(int)
    
        # calls the method which does the calculations
        self.__calc_forces()
    

    def PlotGeometry(self, file_plot):
        """ This method creates a plot of the truss geometry and saves it to \
            the destination specified by 'file_plot'. """
        
        final_pt = np.zeros(2)
        init_pt = np.zeros(2)
        
        # CHANGE THIS HERE FOR GENERAL CASE / TEST OUT
        plt.axis([-1,16,-1,9])
        for i in range(0,self.__numbeams):
            final_pt[0] = self.__joint[self.__beams[i,2]-1][1]
            final_pt[1] = self.__joint[self.__beams[i,2]-1][2]
            init_pt[0] = self.__joint[self.__beams[i,1]-1][1]
            init_pt[1] = self.__joint[self.__beams[i,1]-1][2]
            x_list = np.linspace(init_pt[0],final_pt[0])
            y_list = np.linspace(init_pt[1],final_pt[1])
            # plot each beam
            plt.plot(x_list,y_list, 'b-')
        plt.show()
        plt.savefig(file_plot)
    
    
    def __calc_forces(self):
        """ This method computes the beam forces for the truss of interest. """
    
        # find the number of joints and beams from size of arrays
        self.__numjoints = self.__joint.shape[0]
        self.__numbeams = self.__beams.shape[0]
        num_zerodisp = np.count_nonzero(self.__zerodisp)
        self.__unitvec = {}
        joint_unitvecs = {unitvec_list: [] for unitvec_list in \
                                                        range(self.__numjoints)}
        joint_beams = {beam_list: [] for beam_list in range(self.__numjoints)}
        final_pt = np.zeros(2)
        init_pt = np.zeros(2)
        for i in range(0,self.__numbeams):
            # calculates the unit vectors (Ja->Jb) for each beam
            self.__unitvec.setdefault(i+1)
            final_pt[0] = self.__joint[self.__beams[i][2]-1][1]
            final_pt[1] = self.__joint[self.__beams[i][2]-1][2]
            init_pt[0] = self.__joint[self.__beams[i][1]-1][1]
            init_pt[1] = self.__joint[self.__beams[i][1]-1][2]
            unitvector = final_pt - init_pt
            self.__unitvec[i+1] = unitvector/np.linalg.norm(unitvector)
            # adds the unit vector to a dict of lists of the appropriate joints
            joint_unitvecs[self.__beams[i][1]-1].append(-self.__unitvec[i+1])
            joint_unitvecs[self.__beams[i][2]-1].append(-self.__unitvec[i+1])
            joint_beams[self.__beams[i][1]-1].append(self.__beams[i][0])
            joint_beams[self.__beams[i][2]-1].append(self.__beams[i][0])
        # finding non-zero values for matrix
        data = []
        rows = []
        cols = []
        RHS = np.zeros(2*self.__numjoints)
        total_shape = 2*self.__numjoints, self.__numbeams+2*num_zerodisp
        count_fixed = 0
        # for each joint
        for j in range(0,self.__numjoints):
            B_coeff_list = joint_unitvecs[j]
            beams_list = joint_beams[j]
            count = 0
            # B's for all beams @ joint
            for k in B_coeff_list:
                if not math.isclose(k[0], 0.0):     # X-EQN
                    cols.append(beams_list[count]-1)
                    rows.append(2*(j+1)-2)
                    data.append(k[0])
                if not math.isclose(k[1], 0.0):     # Y-EQN
                    cols.append(beams_list[count]-1)
                    rows.append(2*(j+1)-1)
                    data.append(k[1])
                count += 1
            # Adding Rx & Ry if fixed joint
            if int(self.__joint[j][5])==1:
                count_fixed += 1
                # Rx
                cols.append(self.__numbeams+2*(count_fixed)-2)
                rows.append(2*(j+1)-2)
                data.append(1.0)
                # Ry
                cols.append(self.__numbeams+2*(count_fixed)-1)
                rows.append(2*(j+1)-1)
                data.append(1.0)
            # Adding Fx & Fy to RHS
            Fx = self.__joint[j,3]
            Fy = self.__joint[j,4]
            if not math.isclose(Fx,0.0):
                RHS[2*(j+1)-2] = -Fx
            if not math.isclose(Fy,0.0):
                RHS[2*(j+1)-1] = -Fy

        # Catch warnings as exceptions
        warnings.filterwarnings('error')
        try:
            total_LHS = sp.coo_matrix((data, (rows, cols)), total_shape)
            np.set_printoptions(precision=3,linewidth=100)
            self.__solved_vec = scipy.sparse.linalg.spsolve(total_LHS.tocsr(), \
                                                            RHS)
        except ValueError: # if matrix is overdetermined
            raise RuntimeError("Truss geometry not suitable for static " \
                              "equilibrium analysis")
        except: # if system is singular, aka unstable
            raise RuntimeError("Cannot solve the linear system, unstable " \
                               "truss?")


    def __repr__(self):
        """ This method formats and returns the desired output string as the \
            representation of an instance of the class 'Truss' """

        string = " Beam         Force \n-------------------- \n"
        # add lines for each beam, including number and force
        # string += "Test".format()
        for i in range(0,self.__numbeams):
            string += "    {}      {:9.3f} \n".format(self.__beams[i,0], \
                                                   self.__solved_vec[i])

        return string
