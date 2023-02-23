#include <fstream>
#include "heat.hpp"
#include <iostream>
#include "matvecops.hpp"
#include "sparse.hpp"
#include <string>
#include <vector>

// solves a linear system in CSR format using the CG method, consistent with the
// provided prototype in CGSolver.hp utilizing functions from matvecops.cpp to
// do common operations runs your CG solver function

int CGSolver(SparseMatrix A_in, const std::vector<double> b,
            std::vector<double> &x, const double tol, std::string soln_prefix) {
    
    // Initializing vectors
    std::vector<double> u = x;
    std::vector<double> temp = A_in.MulVec(u);
    std::vector<double> r = SubtractVec(b, temp);
    double L2normr0 = TwoNorm(r);
    std::vector<double> p = r;
    //std::cout << L2normr0 << std::endl;
    
    // Attempting to converge, using pseudocode from problem statement
    unsigned int niter = 0;
    while (niter < 1000){
        niter++;
        double alphnum = VecVec(r, r);
        //std::cout << alphnum << std::endl;
        std::vector<double> alphtemp = A_in.MulVec(p);
        double alphdenom = VecVec(p, alphtemp);
        //std::cout << alphdenom << std::endl;
        double alpha = alphnum/alphdenom;
        u = AddVec(u, MultVecScalar(p, alpha));
        r = SubtractVec(r, MultVecScalar(alphtemp, alpha));
        double L2normr = TwoNorm(r);
        //std::cout << L2normr << std::endl;
        
        if (L2normr/L2normr0 < tol){
            x = u;
            break;
        }
        double alphnum2 = VecVec(r, r);
        double beta = alphnum2/alphnum;
        std::vector<double> betap = MultVecScalar(p, beta);
        p = AddVec(r, betap);
        x = u;
        
        // Write the solution vector to the specified solution file : one value per
        // line, scientific notation, 4 decimal places (every 10 iterations).
        if ((niter-1) % 10 == 0) {
            std::string soln_temp;
            if ((niter-1) < 10){
                soln_temp = soln_prefix + "00" + std::to_string(niter-1) + ".txt";
            }
            else if ((niter >= 10) and (niter < 100)){
                soln_temp = soln_prefix + "0" + std::to_string(niter-1) + ".txt";
            }
            else{
                soln_temp = soln_prefix + std::to_string(niter-1) + ".txt";
            }
            std::ofstream g;
            g.open(soln_temp);
            for (unsigned int n = 0; n < (unsigned int)x.size(); n++) {
                g << x[n] << std::endl; // std::setprecision(4) << std::scientific
            }
            g.close();
        }
    }
    
    std::string soln_temp;
    if (niter < 10){
        soln_temp = soln_prefix + "00" + std::to_string(niter) + ".txt";
    }
    else if ((niter >= 10) and (niter < 100)){
        soln_temp = soln_prefix + "0" + std::to_string(niter) + ".txt";
    }
    else{
        soln_temp = soln_prefix + std::to_string(niter) + ".txt";
    }
    std::ofstream g;
    g.open(soln_temp);
    for (unsigned int n = 0; n < (unsigned int)x.size(); n++) {
        g << x[n] << std::endl; // std::setprecision(4) << std::scientific
    }
    g.close();
    
    if (niter >= 1000){
        return 1;
    }
    std::cout << "SUCCESS: CG solver converged in " << niter << \
        " iterations." << std::endl;
    return 0;
}
