#include <vector>
#include <cmath>

#include "matvecops.hpp"

/* Multiplying a matrix by a vector */
//std::vector<double> MultiplyMatVec(const std::vector<double> val, const
//                                   std::vector<int> row_ptr, const
//                                   std::vector<int> col_idx, const
//                                   std::vector<double> uo) {
//    std::vector<double> output(uo.size());
//    for (unsigned int m = 0; m < (unsigned int)uo.size(); m++){
//        output[m] = 0;
//    }
//    // referenced https://stackoverflow.com/questions/29598299/csr-matrix-matrix-multiplication
//    for (unsigned int i = 0; i < (unsigned int)uo.size(); i++) {
//        for (unsigned int j = (unsigned int)row_ptr[i]; j < (unsigned
//                                                             int)row_ptr[i+1];
//             j++ ) {
//            output[i] = output[i] + val[j]*uo[col_idx[j]];
//        }
//    }
//    return output;
//}

/* Subtracting two vectors */
std::vector<double> SubtractVec(std::vector<double> first, std::vector<double>
                             second) {
    std::vector<double> output(first.size());
    for (unsigned int i = 0; i < (unsigned int)first.size(); i++) {
        output[i] = first[i] - second[i];
    }
    return output;
}

/* Adding two vectors */
std::vector<double> AddVec(std::vector<double> first, std::vector<double>
                                second) {
    std::vector<double> output(first.size());
    for (unsigned int i = 0; i < (unsigned int)first.size(); i++) {
        output[i] = first[i] + second[i];
    }
    return output;
}

/* Multiply two vectors of size 1xN and Nx1 */
double VecVec(std::vector<double> first, std::vector<double> second) {
    double output = 0;
    for (unsigned int i = 0; i < (unsigned int)first.size(); i++) {
            output += first[i]*second[i];
    }
    return output;
}

/* The 2 norm of a vector */
double TwoNorm(std::vector<double> input) {
    double output;
    double sum_squared = 0;
	sum_squared = VecVec(input, input);
    output = sqrt(sum_squared);
    return output;
}

/* Multiplying all elements of vector by scalar */
std::vector<double> MultVecScalar(std::vector<double> input, double scalar) {
    std::vector<double> output(input.size());
    for (unsigned int i = 0; i < (unsigned int)input.size(); i++) {
        output[i] = input[i]*scalar;
    }
    return output;
}
