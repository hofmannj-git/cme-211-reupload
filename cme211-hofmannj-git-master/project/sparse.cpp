#include "COO2CSR.hpp"
#include <iostream>
#include "sparse.hpp"
#include <vector>

/* Method to modify sparse matrix dimensions */
//void SparseMatrix::Resize(int nrows, int ncols){
//
//}

/* Method to add entry to matrix in COO format */
void SparseMatrix::AddEntry(int i_in, int j_in, double val){
    // add to each (if relevant):
    i_idx.push_back(i_in);
    if (j_in < 0){ // from debugging
        std::cout << i_in << " " << j_in << " " << val << std::endl;
    }
    j_idx.push_back(j_in);
    a.push_back(val);
    if (i_in > nrows){
        nrows = i_in;
    }
    if (j_in > ncols){
        ncols = j_in;
    }
}

/* Method to convert COO matrix to CSR format using provided function */
void SparseMatrix::ConvertToCSR(){
    COO2CSR(a,i_idx,j_idx);
}

/* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
std::vector<double> SparseMatrix::MulVec(const std::vector<double> uo){
    std::vector<double> output(uo.size());
    for (unsigned int m = 0; m < (unsigned int)uo.size(); m++){
        output[m] = 0;
    }
    // referenced https://stackoverflow.com/questions/29598299/csr-matrix-matrix-multiplication
    for (unsigned int i = 0; i < (unsigned int)(uo.size()); i++) {
        for (unsigned int j=(unsigned int)i_idx[i]; j<(unsigned int)i_idx[i+1]; j++){
            if (j_idx[j] > (int)(uo.size())){ // from debugging
                std::cout << j_idx[j] << " " << j << std::endl;
            }
            output[i] += a[j]*uo[j_idx[j]];
        }
    }
    return output;
}
