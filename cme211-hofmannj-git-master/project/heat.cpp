#include "CGSolver.hpp"
#include <cmath>
#include <fstream>
#include "heat.hpp"
#include <iostream>
#include "sparse.hpp"
#include <string>
#include <vector>


/* Method to setup Ax=b system */
int HeatEquation2D::Setup(std::string inputfile){
    
    std::ifstream f;
    f.open(inputfile);
    double length, width, h, Tc, Th;
    if (f.is_open()) {
        f >> length >> width >> h >> Tc >> Th;
        f.close();
    }
    
    int num_rows = (int)(width/h);
    int num_col = (int)(length/h);
    double temp_val = -1.0;
    double self_val = 4.0;
    int init_val = 0;
    
    for (int o = 0; o < (num_rows-2)*(num_col-1); o++) {
        b.push_back(0.0);
    }
    
    for (int l = 0; l < (num_col-1); l++) { // col
        for (int m = 0; m < (num_rows-2); m++) { // row
            // ROWS WITH HOT ISOTHERMAL BC
            if (m == 0){
                double temp_b = Th;
                b[init_val] = temp_b;
                if (l==0){ // left-most column
                    A.AddEntry(init_val, init_val+(num_rows-2)*(num_col-2), temp_val); // left
                    A.AddEntry(init_val, init_val+(num_rows-2), temp_val); // right
                    A.AddEntry(init_val, init_val+1, temp_val); // down
                    A.AddEntry(init_val, init_val, self_val); // self
                }
                else if (l==(num_col-2)){ // right-most column
                    A.AddEntry(init_val, init_val-(num_rows-2), temp_val); // left
                    A.AddEntry(init_val, init_val+1, temp_val); // down
                    A.AddEntry(init_val, init_val, self_val); // self
                    A.AddEntry(init_val, init_val-(num_rows-2)*(num_col-2), temp_val); // right
                }
                else{ // every other column
                    A.AddEntry(init_val, init_val-(num_rows-2), temp_val); // left
                    A.AddEntry(init_val, init_val+(num_rows-2), temp_val); // right
                    A.AddEntry(init_val, init_val+1, temp_val); // down
                    A.AddEntry(init_val, init_val, self_val); // self
                }
            }
            // ROWS WITH COOL ISOTHERMAL BC
            else if (m == num_rows-3){
                double temp_b = -Tc*(exp(-10.0*pow((l*h+h-length/2),2.0))-2.0);
                b[init_val] = temp_b;
                if (l==0){ // left-most column
                    A.AddEntry(init_val, init_val+(num_rows-2)*(num_col-2), temp_val); // left
                    A.AddEntry(init_val, init_val+(num_rows-2), temp_val); // right
                    A.AddEntry(init_val, init_val-1, temp_val); // up
                    A.AddEntry(init_val, init_val, self_val); // self
                }
                else if (l==(num_col-2)){ // right-most column
                    A.AddEntry(init_val, init_val-(num_rows-2), temp_val); // left
                    A.AddEntry(init_val, init_val-1, temp_val); // up
                    A.AddEntry(init_val, init_val-(num_rows-2)*(num_col-2), temp_val); // right
                    A.AddEntry(init_val, init_val, self_val); // self
                }
                else{ // every other column
                    A.AddEntry(init_val, init_val-(num_rows-2), temp_val); // left
                    A.AddEntry(init_val, init_val+(num_rows-2), temp_val); // right
                    A.AddEntry(init_val, init_val-1, temp_val); // up
                    A.AddEntry(init_val, init_val, self_val); // self
                }
            }
            // ALL OTHER ROWS WITHOUT BC
            else{
                double temp_b = 0;
                b[init_val] = temp_b;
                if (l==0){ // left-most column
                    A.AddEntry(init_val, init_val+(num_rows-2)*(num_col-2), temp_val); // left
                    A.AddEntry(init_val, init_val+(num_rows-2), temp_val); // right
                    A.AddEntry(init_val, init_val-1, temp_val); // up
                    A.AddEntry(init_val, init_val+1, temp_val); // down
                    A.AddEntry(init_val, init_val, self_val); // self
                }
                else if (l==(num_col-2)){ // right-most column
                    A.AddEntry(init_val, init_val-(num_rows-2), temp_val); // left
                    A.AddEntry(init_val, init_val-1, temp_val); // up
                    A.AddEntry(init_val, init_val+1, temp_val); // down
                    A.AddEntry(init_val, init_val-(num_rows-2)*(num_col-2), temp_val); // right
                    A.AddEntry(init_val, init_val, self_val); // self
                }
                else{ // every other column
                    A.AddEntry(init_val, init_val-(num_rows-2), temp_val); // left
                    A.AddEntry(init_val, init_val+(num_rows-2), temp_val); // right
                    A.AddEntry(init_val, init_val-1, temp_val); // up
                    A.AddEntry(init_val, init_val+1, temp_val); // down
                    A.AddEntry(init_val, init_val, self_val); // self
                }
            }
            init_val++;
        }
    }
    
    A.ConvertToCSR();
    
    return 0;
}

/* Method to solve system using CGsolver */
int HeatEquation2D::Solve(std::string soln_prefix){
    for (unsigned int k = 0; k < b.size(); k++){
        x.push_back(1.0);
    }
    int out_int = CGSolver(A, b, x, 0.00001, soln_prefix);
    return out_int;
}
