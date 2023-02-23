#ifndef matvecops_HPP
#define matvecops_HPP

#include <vector>

/* Multiplying a matrix by a vector. */
//std::vector<double> MultiplyMatVec(const std::vector<double> val, const
//                                   std::vector<int>
//                                   row_ptr, const std::vector<int> col_idx,
//                                   const std::vector<double> uo) ;

/* Subtracting two vectors */
std::vector<double> SubtractVec(std::vector<double> first, std::vector<double>
                                second);

/* Adding two vectors */
std::vector<double> AddVec(std::vector<double> first, std::vector<double>
                           second);

/* Multiply two vectors of size 1xN and Nx1 */
double VecVec(std::vector<double> first, std::vector<double> second);

/* The 2 norm of a vector */
double TwoNorm(std::vector<double> input);

/* Multiplying all elements of vector by scalar */
std::vector<double> MultVecScalar(std::vector<double> input, double scalar);

#endif /* matvecops_hpp */
