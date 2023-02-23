class Airfoil:
    """ This class Airfoil contains six methods: \n
        '__init__' - this method initializes the class based on the input \
            directory, and calls the 'load_airfoil_data' method \n
        '__load_airfoil_data' - this method loads the data from the input \
            directory, and creates the desired data structures \n
        'calc_chord' - this method calculates the airfoil chord length and \
            stores it \n
        'calc_alpha' - this method calculates the lift coefficients and \
            stagnation points for all angles of incidence in the data \n
        'call_calc' -  this method calls the two calculation methods, \
            'calc_chord' and 'calc_alpha', and itself is called after loading \
            the data in 'load_airfoil_data' \n
        '__repr__' -  this method formats the outputs (alphas, cls, and \
            stagnation points) in the desired string output format and changes \
            the class representation to this output, so that print(Airfoil \
            type ) prints the desired output """
    

    def __init__(self, inputdir):
        """ This initialization method takes in the input directory name \
            'inputdir' and calls the method 'load_airfoil_data'. """
        
        self.__load_airfoil_data(inputdir)

    
    def __load_airfoil_data(self, inputdir):
        """ This method loads the data from the desired input directory and \
            makes the following outputs as subsets of self: \n
            '__airfoil_name': the name of the airfoil, from the xy.dat file \n
            '__x_list': the list of the x-values for the airfoil geometry \n
            '__y_list': the list of the y-values for the airfoil geometry \n
            '__alpha_list': a list of all alpha values in for the airfoil \n
            '__cp_dict': a dictionary containing the pressure coefficient data \
                (list, value) for all alphas (keys) """
        
        import glob
        import sys
        import os.path
        
        # loads the xy.dat file
        self.__x_list = [0]
        self.__y_list = [0]
        count = 0
        xy_name = inputdir + "/xy.dat"
        
        # GENERATE EXCEPTIONS: nonexistence errors
        if not os.path.exists(sys.path[0] + "/" + inputdir):
            raise RuntimeError("The argument to the class type 'Airfoil' is " \
                               "not a valid directory.")
        if not os.path.exists(sys.path[0] + "/" + xy_name):
            raise RuntimeError("There does not exist an 'xy.dat' file in the " \
                               "directory specified by the input argument.")
        
        try:
            with open(xy_name, "r") as f:
                for line in f:
                    if "NACA" in line:
                        self.__airfoil_name = line
                    else:
                        # the x & y lists are each in the same order
                        if count == 0:
                            self.__x_list[count] = float(line.split()[0])
                            self.__y_list[count] = float(line.split()[1])
                            count += 1
                        else:
                            self.__x_list.append(float(line.split()[0]))
                            self.__y_list.append(float(line.split()[1]))
                            count += 1
        except: # if any error raised at all in above 'try' section
            raise RuntimeError("There was an error while reading data from " \
                               "the xy.dat file.")

        # loads all alpha_.dat files present
        count = 0
        count_alph = 0
        self.__cp_dict = {}
        self.__alpha_list = [0]
        exist_alpha = glob.glob(sys.path[0] + "/" + inputdir + "/alpha*")
        
        # GENERATE EXCEPTION: existence error
        if not exist_alpha:
            raise RuntimeError("There do not exist any 'alpha*.dat' files in " \
                               "the directory specified by the input argument.")
        
        for alphafile in exist_alpha: # for all alpha files present
            # makes the alpha list
            alpha = alphafile[68:-4] # getting rid of the extra characters
            try:
                if count_alph == 0:
                    if "+" in alpha: # to get rid of the plus signs
                        alpha = float(alpha[1:])
                        self.__alpha_list[count_alph] = alpha
                    else:
                        alpha = float(alpha)
                        self.__alpha_list[count_alph] = alpha
                    count_alph += 1
                else:
                    if "+" in alpha: # to get rid of the plus signs
                        alpha = float(alpha[1:])
                        (self.__alpha_list).append(alpha)
                    else:
                        alpha = float(alpha)
                        (self.__alpha_list).append(alpha)
                # makes the pressure coefficient dictionary from the data
                self.__cp_dict[alpha] = [0]
                with open(alphafile, "r") as f:
                    for line in f:
                        if "#" in line:
                            continue
                        else:
                            if count == 0:
                                self.__cp_dict[alpha][count] = float(line)
                                count += 1
                            else:
                                (self.__cp_dict[alpha]).append(float(line))
            except: # if any error raised at all in above 'try' section
                raise RuntimeError("There was an error while reading data " \
                                   "for an alpha*.dat file.")

        self.__alpha_list.sort() # sort the list for later printing
        
        # calls the method which calls the calculations
        self.__call_calc()

        
    def __calc_chord(self):
        """ This method calculates the chord length for the airfoil, given the \
            loaded x and y positions. \n
            '__chord_length': the chord length of the airfoil \n """
        
        import math
        
        # find the min & max coordinates of the airfoil
        xmin = min(self.__x_list)
        ymin = self.__y_list[(self.__x_list).index(xmin)]
        xmax = max(self.__x_list)
        ymax = self.__y_list[(self.__x_list).index(xmax)]
    
        self.__chord_length = math.sqrt( (xmax - xmin)**2 + (ymax - ymin)**2 )

    
    def __calc_alphas(self):
        """ This method calculates the lift coefficients and stagnation points \
            for each pressure coefficient for the airfoil of interest. \n
            '__cl': a dictionary of lift coefficients (values) for each alpha \
                (keys) \n
            '__stag_x': a dictionary of x-coordinates of the stagnation points \
                (values) for each alpha (keys) \n
            '__stag_y': a dictionary of y-coordinates of the stagnation points \
                (valuses) for each alpha (keys) \n
            '__stag_cp': a dictionary of the pressure coefficients at the \
                stagnation point (values) for each alpha (keys) """
    
        import math
    
        # for a given angle of attack (input), calculate the cl & stag pts
        self.__cl = {}
        self.__stag_x = {}
        self.__stag_y = {}
        self.__stag_cp = {}
        for alpha in self.__alpha_list:
            # calculating the lift coefficient
            for m in range(0,len(self.__x_list)-1):
                Cp = self.__cp_dict[alpha][m]
                dely = self.__y_list[m + 1] - self.__y_list[m]
                delx = self.__x_list[m + 1] - self.__x_list[m]
                if m == 0:
                    cx = -Cp * dely / self.__chord_length
                    cy = Cp * delx / self.__chord_length
                else:
                    cx += -Cp * dely / self.__chord_length
                    cy += Cp * delx / self.__chord_length

            alpha_rad = math.radians(alpha)
            self.__cl[alpha] = cy * math.cos(alpha_rad) - \
                                cx * math.sin(alpha_rad)

            # calculating the stagnation point - utilizing a technique found \
            # online from Andrew Clark (line 183): stackoverflow.com/ \
            # questions/9706041/finding-index-of-an-item-closest-to-the-value \
            # -in-a-list-thats-not-entirely-sort
            index_cp, cp_1 = min(enumerate(self.__cp_dict[alpha]), key=lambda \
                                 x: abs(x[1]-1.0)) # finding Cp closest to 1.0
            self.__stag_x[alpha] = (self.__x_list[index_cp + 1] + \
                                  self.__x_list[index_cp])/2
            self.__stag_y[alpha] = (self.__y_list[index_cp + 1] + \
                                  self.__y_list[index_cp])/2
            self.__stag_cp[alpha] = cp_1
    
    
    def __call_calc(self):
        """ This method calls the methods for the calculation of the chord \
            length and stagnation points for each alpha. """
    
        self.__calc_chord()
        self.__calc_alphas()
    
    
    def __repr__(self):
        """ This method formats and returns the desired output string as the \
            representation of an instance of the class 'Airfoil' """
        
        string = "Test case: {} \n  alpha     cl           stagnation pt  " \
            "     \n  _____  _______  __________________________ \n" \
            .format(self.__airfoil_name)
            
        for alpha in self.__alpha_list:
            if alpha < 0 and self.__cl[alpha] < 0 and self.__stag_y[alpha] < 0:
                string += ("  {:0.2f}  {:0.4f}  ( {:0.4f}, {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.__cl[alpha], \
                                              self.__stag_x[alpha], \
                                              self.__stag_y[alpha], \
                                              self.__stag_cp[alpha] )
            elif alpha < 0 and self.__cl[alpha] >= 0 and \
                                                    self.__stag_y[alpha] < 0:
                string += ("  {:0.2f}   {:0.4f}  ( {:0.4f}, {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.__cl[alpha], \
                                              self.__stag_x[alpha], \
                                              self.__stag_y[alpha], \
                                              self.__stag_cp[alpha] )
            elif alpha < 0 and self.__cl[alpha] < 0 and \
                                                    self.__stag_y[alpha] >= 0:
                string += ("  {:0.2f}  {:0.4f}  ( {:0.4f},  {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.__cl[alpha], \
                                               self.__stag_x[alpha], \
                                               self.__stag_y[alpha], \
                                               self.__stag_cp[alpha] )
            elif alpha >= 0 and self.__cl[alpha] < 0 and \
                                                    self.__stag_y[alpha] < 0:
                string += ("   {:0.2f}  {:0.4f}  ( {:0.4f}, {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.__cl[alpha], \
                                               self.__stag_x[alpha], \
                                               self.__stag_y[alpha], \
                                               self.__stag_cp[alpha] )
            elif alpha < 0 and self.__cl[alpha] >= 0 and \
                                                    self.__stag_y[alpha] >= 0:
                string += ("  {:0.2f}   {:0.4f}  ( {:0.4f},  {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.cl[alpha], \
                                               self.stag_x[alpha], \
                                               self.stag_y[alpha], \
                                               self.stag_cp[alpha] )
            elif alpha >= 0 and self.__cl[alpha] < 0 and \
                                                    self.__stag_y[alpha] >= 0:
                string += ("   {:0.2f}  {:0.4f}  ( {:0.4f},  {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.__cl[alpha], \
                                               self.__stag_x[alpha], \
                                               self.__stag_y[alpha], \
                                               self.__stag_cp[alpha] )
            elif alpha >= 0 and self.__cl[alpha] >= 0 and \
                                                    self.__stag_y[alpha] < 0:
                string += ("   {:0.2f}   {:0.4f}  ( {:0.4f}, {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.__cl[alpha], \
                                               self.__stag_x[alpha], \
                                               self.__stag_y[alpha], \
                                               self.__stag_cp[alpha] )
            elif alpha >= 0 and self.__cl[alpha] >= 0 and \
                                                    self.__stag_y[alpha] >= 0:
                string += ("   {:0.2f}   {:0.4f}  ( {:0.4f},  {:0.4f})  " + \
                           "{:0.4f}\n").format( alpha, self.__cl[alpha], \
                                               self.__stag_x[alpha], \
                                               self.__stag_y[alpha], \
                                               self.__stag_cp[alpha] )
        return string
