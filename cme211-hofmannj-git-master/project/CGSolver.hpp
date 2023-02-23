#ifndef CGSOLVER_HPP
#define CGSOLVER_HPP

#include "heat.hpp"
#include "sparse.hpp"
#include <string>
#include <vector>

/* Function that implements the CG algorithm for a linear system
 *
 * Ax = b
 *
 * where A is in CSR format.  The starting guess for the solution
 * is provided in x, and the solver runs a maximum number of iterations.
 */

int CGSolver(SparseMatrix A_in,
             const std::vector<double> b,
             std::vector<double> &x,
             const double        tol,
             std::string soln_prefix);

//int CGSolver(std::vector<double> &val,
//             std::vector<int>    &row_ptr,
//             std::vector<int>    &col_idx,
//             std::vector<double> &b,
//             std::vector<double> &x,
//             const double        tol);

#endif /* CGSOLVER_HPP */
