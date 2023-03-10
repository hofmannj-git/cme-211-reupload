#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>

class SparseMatrix
{
  private:
    std::vector<int> i_idx;
    std::vector<int> j_idx;
    std::vector<double> a;
    int ncols = 0;
    int nrows = 0;

    /* TODO: Add any additional private data attributes and/or methods  you need */


  public:
    /* Method to modify sparse matrix dimensions */
    //void Resize(int nrows, int ncols);

    /* Method to add entry to matrix in COO format */
    void AddEntry(int i_in, int j_in, double val);

    /* Method to convert COO matrix to CSR format using provided function */
    void ConvertToCSR();

    /* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
    std::vector<double> MulVec(const std::vector<double> uo);

    /* TODO: Add any additional public methods you need */
    
};

#endif /* SPARSE_HPP */
