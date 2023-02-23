#include "CGSolver.hpp"
#include "COO2CSR.hpp"
#include <fstream>
#include "heat.hpp"
#include <iostream>
#include <iomanip>
#include <string>
#include <tuple>
#include <vector>

int main(int argc , char * argv []){
    
    // Confirm that appropriate command line arguments were provided and if not provide a usage message and exit.
    if (argc != 3) {
        std::cout << "Usage: \n ./main <input file> <soln prefix>" << std::endl;
        return 0;
    }
    std::string inputname = argv[1];
    std::string outputname = argv[2];
    
    /* Setup 2D heat equation system */
    HeatEquation2D sys;
    int status = sys.Setup(inputname);
    if (status)
    {
        std::cerr << "ERROR: System setup was unsuccessful!" << std::endl;
        return 1;
    }
    
    /* Solve system using CG */
    status = sys.Solve(outputname);
    if (status)
    {
        std::cerr << "ERROR: System solve was unsuccessful!" << std::endl;
        return 1;
    }
    
    return 0;
    
}
