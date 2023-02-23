class Airfoil:
    """ This class _____ """
    

    def __init__(self, inputdir):
        """ This initialization method takes in the input directory name \
            'inputdir' and calls the method 'load_airfoil_data'. """
        
        self.load_airfoil_data(inputdir)

    
    def load_airfoil_data(self, inputdir):
        """ This method loads the data from the desired input directory and \
            makes the following outputs as methods of self: \n
            'airfoil_name': the name of the airfoil, from the xy.dat file \n
            'x_list': the list of the x-values for the airfoil geometry \n
            'y_list': the list of the y-values for the airfoil geometry \n
            'alpha_list': a list of all alpha values in for the given airfoil \n
            'cp_dict': a dictionary containing the pressure coefficient data \
                (list, value) for all alphas (keys) """
        
        import glob
        import sys
        
        # loads the xy.dat file
        self.x_list = [0]
        self.y_list = [0]
        count = 0
        xy_name = inputdir + "/xy.dat"
        with open(xy_name, "r") as f:
            for line in f:
                if "NACA" in line:
                    self.airfoil_name = line
                else:
                    # the x & y lists are each in the same order
                    if count == 0:
                        self.x_list[count] = float(line.split()[0])
                        self.y_list[count] = float(line.split()[1])
                        count += 1
                    else:
                        self.x_list.append(float(line.split()[0]))
                        self.y_list.append(float(line.split()[1]))
                        count += 1

        # loads all alpha_.dat files present
        count = 0
        count_alph = 0
        self.cp_dict = {}
        self.alpha_list = [0]
        exist_alpha = glob.glob(sys.path[0] + "/" + inputdir + "/alpha*")
        for alphafile in exist_alpha:
            alpha = alphafile[68:-4]
            if count_alph == 0:
                if "+" in alpha: # to get rid of the plus signs
                    alpha = float(alpha[1:])
                    self.alpha_list[count_alph] = alpha
                else:
                    alpha = float(alpha)
                    self.alpha_list[count_alph] = alpha
                count_alph += 1
            else:
                if "+" in alpha: # to get rid of the plus signs
                    alpha = float(alpha[1:])
                    (self.alpha_list).append(alpha)
                else:
                    alpha = float(alpha)
                    (self.alpha_list).append(alpha)
            self.cp_dict[alpha] = [0]
            with open(alphafile, "r") as f:
                for line in f:
                    if "#" in line:
                        continue
                    else:
                        if count == 0:
                            self.cp_dict[alpha][count] = float(line)
                            count += 1
                        else:
                            (self.cp_dict[alpha]).append(float(line))
    
        # calls the next method in the calculation
        print((self.cp_dict).keys())
        self.calc_chord()

        
    def calc_chord(self):
        """ This method calculates the chord length for the airfoil, given the \
            loaded x and y positions. \n
            'chord_length': the chord length of the airfoil \n """
        
        import math
    
        xmin = min(self.x_list)
        ymin = self.y_list[(self.x_list).index(xmin)]
        xmax = max(self.x_list)
        ymax = self.y_list[(self.x_list).index(xmax)]
    
        self.chord_length = math.sqrt( (xmax - xmin)**2 + (ymax - ymin)**2 )
    
        # calls the next method in the calculation
        self.calc_alphas()

    
    def calc_alphas(self):
        """ This method calculates the lift coefficients and stagnation points \
            for each pressure coefficient for the airfoil of interest. \n
            '___': ___ \n
            '___': ___ """
    
        import math
    
        # for a given angle of attack (input), calculate the cl & stag pts
        self.cl = {}
        self.stag_x = {}
        self.stag_y = {}
        self.stag_cp = {}
        for alpha in self.alpha_list:
            # calculating the lift coefficient
            for m in range(0,len(self.x_list)-1):
                Cp = self.cp_dict[alpha][m]
                dely = self.y_list[m + 1] - self.y_list[m]
                delx = self.x_list[m + 1] - self.x_list[m]
                if m == 0:
                    cx = -Cp * dely / self.chord_length
                    cy = Cp * delx / self.chord_length
                else:
                    cx += -Cp * dely / self.chord_length
                    cy += Cp * delx / self.chord_length

            alpha_rad = math.radians(alpha)
            self.cl[alpha] = cy * math.cos(alpha_rad) - cx * math.sin(alpha_rad)

            # calculating the stagnation point - utilizing a technique found \
            # online from Andrew Clark: stackoverflow.com/questions/9706041/ \
            # finding-index-of-an-item-closest-to-the-value-in-a-list-thats- \
            # not-entirely-sort
            index_cp, cp_1 = min(enumerate(self.cp_dict[alpha]), key=lambda x: \
                          abs(x[1]-1.0)) # finding the Cp closest to 1.0
            self.stag_x[alpha] = (self.x_list[index_cp + 1] + \
                                  self.x_list[index_cp])/2
            self.stag_y[alpha] = (self.y_list[index_cp + 1] + \
                                  self.y_list[index_cp])/2
            self.stag_cp[alpha] = cp_1
    
    
    def get_values(self):
        """ This method ____ \n
            '___': ___ \n
            '___': ___ """
    
    
    def __repr__(self):
        """ This method formats and returns the desired output string as the \
            representation of the class 'Airfoil' """
        
        string = "Test case: {} \n  alpha     cl           stagnation pt  " \
            "     \n  _____  _______  __________________________ \n" \
            .format(self.airfoil_name)
            
        for alpha in self.alpha_list:
            if alpha < 0:
                string += "  {:0.2f}  {:0.4f}  ({:0.4f}, {:0.4f})  {:0.4f}" \
                    "\n".format( alpha, alpha, alpha, alpha, -1*alpha)
            else:
                string += "   {:0.2f}   {:0.4f}  ( {:0.4f},  {:0.4f})  {:0.4f}" \
                    "\n" .format( alpha, alpha, alpha, alpha, alpha)

        return string

    
# needs to print, for each angle of attack: lift coefficient (calculated),
# coordinates (average of points defining panel) and pressure coefficient
# (closest value to 1.0) of the stagnation point.

# need to include part to test function errors (outside of methods)

